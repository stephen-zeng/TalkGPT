from blinker import Signal
import os
import json
import websocket
import threading
import time

gptSignal = Signal('gptSignal')

def on_open(ws):
    print("Connected to OpenAI")
    gptSignal.send(0, operation='connected', data=0)

def on_message(ws, data):
    print("Receive data from OpenAI")
    print(data)

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

def gptInit(key, model):
    global ws
    url = "wss://api.openai.com/v1/realtime?model=" + model
    headers = [
        "Authorization: Bearer " + key,
        "OpenAI-Beta: realtime=v1"
    ]
    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
    )
