from blinker import Signal
from core.methods import modelNewMemory, modelEditMemory
import json
import websocket
import threading

gptSignal = Signal('gptSignal')
global conversationUUID
global memoryUUID
conversationUUID = 'None'
memoryUUID = 'None'

# GPT的发送操作
def gptNewConversation(data):
    global conversationUUID
    conversationUUID = data['uuid']
    event = {
        "object": "realtime.session",
        "model": data['model'],
        "instructions": data['instruction'],
        "voice": data['voice'],
        "input_audio_format": "g711_alaw",
        "output_audio_format": "pcm16",
        "temperature": data['temperature'],
    }
    ws.send(json.dumps(event))

def gptUpdateConversation(data):
    event = {
        "type": "session.update",
        "session": {
            "model": data['model'],
            "instructions": data['instruction'],
            "temperature": data['temperature'],
        }
    }
    ws.send(json.dumps(event))

def gptNewMemory(data):
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
    event = {
        "type": "conversation.item.delete",
        "item_id": data['serverid']
    }
    ws.send(json.dumps(event))

def gptNewVoice():
    event = {
        "type": "input_audio_buffer.clear"
    }
    ws.send(json.dumps(event))
    global memoryUUID
    memoryUUID = modelNewMemory({
        "message": "waiting for transcription",
        "voice": "None",
        "role": True,
        "serverid": "None",
        "uuid": conversationUUID,
    })['uuid']
    # local voice process needed

def gptAddVoice(data):
    event = {
        "type": "input_audio_buffer.append",
        "audio": data['audio'],
    }
    ws.send(json.dumps(event))
    # local voice process needed

def gptSendVoice():
    event = {
        "type": "input_audio_buffer.commit"
    }
    ws.send(json.dumps(event))
    modelEditMemory({
        "uuid": memoryUUID,
        "serverid": "None",
        "message": "None",
        "voice": "The local voice link",
    })
    # local voice process needed

def gptRequire():
    event = {
        "type": "response.create",
    }
    ws.send(json.dumps(event))

# GPT的接收操作
def gptMemoryCreated(data): # item
    modelEditMemory({
        "uuid": memoryUUID,
        "serverid": data['id'],
        "message": "None",
        "voice": "None"
    })

def gptMemoryTranscription(data):
    modelEditMemory({
        "uuid": "None",
        "serverid": data['item_id'],
        "voice": "None",
        "message": data['transription']
    })

def gptNewResponse(data):
    global memoryUUID
    memoryUUID = modelNewMemory({
        "uuid": conversationUUID,
        "serverid": data['id'],
        "role": True,
        "voice": "None",
        "message": "Waiting for transcription"
    })['uuid']
    # need to process the audio

def gptResponseAudioDelta(data):
    # need to process the audio
    return

def gptResponseAudioDone(data):
    # need to process the audio
    modelEditMemory({
        "uuid": "None",
        "serverid": data['item_id'],
        "voice": "the local voice link",
        "message": "None"
    })

def gptResponseTranscription(data):
    modelEditMemory({
        "uuid": "None",
        "serverid": data['item_id'],
        "message": data['delta'],
        "voice": "None"
    })

def on_message(ws, data):
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