from blinker import Signal
from core.methods import addVoiceTranscription, editMemory, newMemory
import json
import uuid
import websocket
import threading

gptSignal = Signal('gptSignal')

def on_open(ws):
    print("Connected to OpenAI")
    gptSignal.send(0, operation='connected', data=0)

# 1.3 剩下音频部分还没有处理
def on_message(ws, data):
    print("Receive data from OpenAI")
    print(data)
    match data['type']:
        case "conversation.item.input_audio_transcription.completed":
            addVoiceTranscription(data['item_id'], data['transcipt'])
        case "response.created":
            global memoryUUID
            memoryUUID = newMemory({
                "role": True,
                "message": "",
                "voice": "",
                "uuid": conversationUUID
            })
        case "response.text.delta":
            editMemory({
                    "id": data['response_id'],
                    "text": data['delta'],
                    "audio": "",
                    "uuid": memoryUUID,
            })
        case _:
            print('Other Signal')
            
            

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

def gptNewConversation(data, uuid):
    event = {
        "id": uuid,
        "object": "realtime.session",
        "model": data['model'],
        "instructions": data['instruction'],
        "voice": data['voice'],
        "temperature": data['temperature'],
    }
    global conversationUUID
    conversationUUID = data['uuid']
    ws.send(json.dumps(event))

def gptEditConversation(data):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": "session_update",
        "session": {
            "model": data['model'],
            "instructions": data['instruction'],
            "temperature": data['temperature'], 
        }
    }
    ws.send(json.dumps(event))

def gptNewMemory(data, typ, audio):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": "conversation.item.create",
        "item": {
            "id": data['uuid'],
            "type": "message",
            "role": "user",
            "content": [],
        }
    }
    if (typ == "text"):
        memory = {
            "type": "input_text",
            "text": data['message'],
        }
    else :
        memory = {
            "type": "input_audio",
            "audio": audio, # Base64 encoded
        }
    event["item"]["content"].append(memory)
    ws.send(json.dumps(event))

def gptDelMemory(data):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": "conversation.item.delete",
        "item_id": data['uuid'],
    }
    ws.send(json.dumps(event))

def gptGetResponse():
    event = {
        "event_id": str(uuid.uuid4()),
        "type": "response.create",
    }

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