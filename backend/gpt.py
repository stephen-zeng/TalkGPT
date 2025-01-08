from blinker import Signal
from core.methods import modelNewMemory, modelEditMemory, modelEditConversation
from audio import audioAdd, audioEnd, audioDel
import json
import websocket
import threading
import time
import requests


gptSignal = Signal('gptSignal')
global conversationUUID
global memoryUUID
conversationUUID = 'None'
memoryUUID = 'None'

# GPT的发送操作
def gptNewConversation(data):
    print("gptNewConversation")
    print(data)
    global conversationUUID
    conversationUUID = data['uuid']
    event = {
        "model": data['model'],
        "voice": data['voice'],
        "turn_detection": None,
    }
    headers = {
        'Authorization': f'Bearer {apikey}',
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.openai.com/v1/realtime/sessions', headers=headers, json=event).json()
    modelEditConversation({
        'uuid': conversationUUID,
        'key': response['client_secret']['value']})
    print("New Conversation Created")
    print(response)
    event = {
        "type": "session.update",
        "session": {
            "input_audio_format": "g711_alaw",
            "turn_detection": None,
        }
    }
    ws.send(json.dumps(event))
    print("Turned off VAD")

def gptChangeConversation(data):
    print("gptChangeConvesation")
    print(data)
    # to be continued

def gptUpdateConversation(data):
    print("gptUpdateConversation")
    print(data)
    event = {
        "type": "session.update",
        "session": {
            "model": data['model'],
            "instructions": data['instruction'],
            "temperature": data['temperature'],
            "input_audio_format": "g711_alaw",
            "output_audio_format": "pcm16",
            "turn_detection": None,
        }
    }
    ws.send(json.dumps(event))

def gptNewMemory(data):
    print("gptNewMemory")
    print(data)
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
    print(data)
    event = {
        "type": "conversation.item.delete",
        "item_id": data['serverid']
    }
    audioDel(data)
    ws.send(json.dumps(event))

def gptNewVoice(): # 来自前端
    print("gptNewVoice")
    gptCancelVoice()
    global memoryUUID
    memoryUUID = modelNewMemory({
        "message": "waiting for transcription",
        "voice": "None",
        "role": False,
        "serverid": "None",
        "uuid": conversationUUID,
    })['uuid']

def gptAddVoice(data): # 来自前端，是alaw
    print("gptAddVoice")
    print(data)
    event = {
        "type": "input_audio_buffer.append",
        "audio": data['audio'],
    }
    ws.send(json.dumps(event))
    audioAdd({
        "uuid": memoryUUID,
        "audio": data['audio']
    })

def gptSendVoice():
    print("gptSendVoice")
    modelEditMemory({
        "uuid": memoryUUID,
        "voice": audioEnd({
            "uuid": memoryUUID,
            "frame": 44100,
        }),
    })

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
    print(data)
    modelEditMemory({
        "uuid": memoryUUID,
        "serverid": data['id'],
    })

def gptMemoryTranscription(data):
    print("gptMemoryTranscription")
    print(data)
    modelEditMemory({
        "serverid": data['item_id'],
        "message": data['transription']
    })

def gptNewResponse(data):
    print("gptNewResponse")
    print(data)
    global memoryUUID
    memoryUUID = modelNewMemory({
        "uuid": conversationUUID,
        "serverid": data['id'],
        "role": True,
        "voice": "None",
        "message": "Waiting for transcription"
    })['uuid']

def gptResponseAudioDelta(data):
    # print("gptResponseAudioDelta")
    # print(data)
    audioAdd({
        "uuid": memoryUUID,
        "audio": data['delta'],
    })

def gptResponseAudioDone(data):
    print("gptResponseAudioDone")
    print(data)
    modelEditMemory({
        "uuid": memoryUUID,
        "frame": audioEnd({
            "uuid": memoryUUID,
            "frame": 24000,
        }),
    })

def gptResponseTranscription(data):
    print("gptResponseTranscription")
    print(data)
    modelEditMemory({
        "uuid": memoryUUID,
        "message": data['delta'],
    })

def on_message(ws, receive):
    data = json.loads(receive)
    print("Receive data from OpenAI")
    print(data)
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
        case "response.audio_transcript.delta":
            gptResponseTranscription(data)
        case "response.done":
            gptSignal.send(0, operation="replied", data=0)
        case _:
            print('Other Message')

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
    global apikey
    apikey = key
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview-2024-12-17"
    headers = [
        "Authorization: Bearer " + apikey,
        "OpenAI-Beta: realtime=v1"
    ]
    global ws
    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
    )