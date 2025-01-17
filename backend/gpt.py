from blinker import Signal
from core.methods import modelNewMemory, modelEditMemory, modelEditConversation
from audio import audioAdd, audioEnd, audioDel
from dotenv import load_dotenv
import json
import websocket
import threading
import time
import os
load_dotenv()
if os.getenv('PROXY') is not None:
    os.environ['HTTP_PROXY'] = os.getenv('PROXY')
    os.environ['HTTPS_PROXY'] = os.getenv('PROXY')


gptSignal = Signal('gptSignal')
global conversationUUID
global memoryUUID
global memoryUUIDUserVoice
conversationUUID = 'None'
memoryUUID = 'None'
memoryUUIDUserVoice = 'None'

# GPT的发送操作
def gptNewConversation(data):
    print("gptNewConversation")
    
    gptUpdateConversation(data)

def gptUpdateConversation(data):
    print("gptUpdateConversation")
    global conversationUUID
    conversationUUID = data['uuid']
    event = {
        "type": "session.update",
        "session": {
            "model": data['model'],
            "instructions": data['instruction'],
            "temperature": data['temperature'],
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "turn_detection": None,
            "voice": data['voice'],
            "input_audio_transcription": {
                "model": "whisper-1"
            },
        }
    }
    gptSignal.send(0, operation="inited", data=0)
    ws.send(json.dumps(event))

def gptNewMemory(data):
    print("gptNewMemory")
    global memoryUUID
    memoryUUID = data['uuid']
    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_text",
                "text": data['message']
            }]
        }
    }
    ws.send(json.dumps(event))

def gptDelMemory(data):
    print("gptDelMemory")
    event = {
        "type": "conversation.item.delete",
        "item_id": data['serverid']
    }
    audioDel(data)
    ws.send(json.dumps(event))

def gptNewVoice(): # 来自前端
    print("gptNewVoice")
    global memoryUUIDUserVoice
    global memoryUUID
    memoryUUIDUserVoice = modelNewMemory({
        "message": "Waiting for transcription",
        "voice": "None",
        "role": False,
        "serverid": "None",
        "uuid": conversationUUID,
    })['uuid']
    memoryUUID = memoryUUIDUserVoice

def gptAddVoice(data): # 来自前端，是alaw
    print("gptAddVoice")
    event = {
        "type": "input_audio_buffer.append",
        "audio": data['audio'],
    }
    ws.send(json.dumps(event))
    audioAdd({
        "uuid": memoryUUIDUserVoice,
        "audio": data['audio']
    })

def gptSendVoice():
    print("gptSendVoice")
    modelEditMemory({
        "uuid": memoryUUIDUserVoice,
        "voice": audioEnd({
            "uuid": memoryUUIDUserVoice,
        }),
    })
    event = {
        "type": "input_audio_buffer.commit"
    }
    ws.send(json.dumps(event))


def gptCancelVoice():
    print("gptCancelVoice")
    event = {
        "type": "input_audio_buffer.commit"
    }
    ws.send(json.dumps(event))
    

def gptRequire():
    print("gptRequire")
    event = {
        "type": "response.create",
    }
    ws.send(json.dumps(event))

# GPT的接收操作
def gptMemoryCreated(data): # item
    print("gptMemoryCreated")
    modelEditMemory({
        "uuid": memoryUUID,
        "serverid": data['id'],
    })

def gptMemoryTranscription(data):
    print("gptMemoryTranscription")
    modelEditMemory({
        "uuid": memoryUUIDUserVoice,
        "message": data['transcript'].rstrip()
    })

def gptNewResponse(data):
    print("gptNewResponse")
    global memoryUUID
    memoryUUID = modelNewMemory({
        "uuid": conversationUUID,
        "serverid": data['id'],
        "role": True,
        "voice": "None",
        "message": "Waiting for transcription"
    })['uuid']
    gptSignal.send(0, operation="newAudio", data=0)

def gptResponseAudioDelta(data):
    print("gptResponseAudioDelta")
    audioAdd({
        "uuid": memoryUUID,
        "audio": data['delta'],
    })
    gptSignal.send(0, operation="addAudio", data={
        'audio': data['delta']
    })

def gptResponseAudioDone(data):
    print("gptResponseAudioDone")
    modelEditMemory({
        "uuid": memoryUUID,
        "voice": audioEnd({
            "uuid": memoryUUID,
        }),
    })

def gptResponseTranscription(data):
    print("gptResponseTranscription")
    modelEditMemory({
        "uuid": memoryUUID,
        "message": data['delta'],
    })

def on_message(ws, receive):
    data = json.loads(receive)
    print("Receive data from OpenAI")
    match data['type']:
        case "conversation.item.created":
            gptMemoryCreated(data['item'])
        case "conversation.item.input_audio_transcription.completed":
            gptMemoryTranscription(data)
        case "response.created":
            gptNewResponse(data['response'])
        case "response.audio.delta":
            gptResponseAudioDelta(data)
        case "response.audio.done":
            gptResponseAudioDone(data)
            gptSignal.send(0, operation="replied", data=0)
        case "response.audio_transcript.delta":
            gptResponseTranscription(data)
            gptSignal.send(0, operation="replying", data=0)
        case "response.done":
            gptSignal.send(0, operation="replied", data=0)

# GPT的连接操作

def on_open(ws):
    print("Connected to OpenAI")
    gptSignal.send(0, operation='connected', data=0)
            
def connect():
    ws.keep_running = True
    ws.run_forever()

def gptConnect():
    global server
    server = threading.Thread(target=connect)
    server.start()

def gptDisconnect():
    if ('server' not in globals()):
        return
    if (server.is_alive() == False):
        return
    ws.keep_running = False
    ws.close()
    server.join()
    print('Disconnect from OpenAI')
    time.sleep(1)
    gptSignal.send(0, operation='disconnected', data=0)

def gptInit(key):
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview-2024-12-17"
    headers = [
        "Authorization: Bearer " + key,
        "OpenAI-Beta: realtime=v1"
    ]
    global ws
    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
    )