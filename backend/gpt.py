from blinker import Signal
from core.methods import modelNewMemory
import json
import uuid
import websocket
import threading

gptSignal = Signal('gptSignal')
global conversationUUID
global memoryUUID
conversationUUID = 'None'
memoryUUID = 'None'

# GPT端的被动操作有：

# GPT主动发出的操作：

def on_message(ws, data):
    print("Receive data from OpenAI")
    print(data)
    match data['type']:
        case "":

        case _:
            print('Other Message')

# GPT连接上的操作
# 被动操作：初始化、连接、断开连接
# 主动操作：报告连接成功

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