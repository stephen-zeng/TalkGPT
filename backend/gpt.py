import os
import json
import websocket
import threading
import time
from multiprocessing import Process

def on_open(ws):
    print("Connected to OpenAI")

def on_message(ws, data):
    print("Receive data from OpenAI")
    print(data)

def setup():
    global ws
    ws = websocket.WebSocketApp(
        url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
    )
    ws.run_forever()
    ws.close()

def gptInit(key, model):
    global url
    global headers
    global gpt_server
    url = "wss://api.openai.com/v1/realtime?model=" + model
    headers = [
        "Authorization: Bearer " + key,
        "OpenAI-Beta: realtime=v1"
    ]
    gpt_server = Process(target=setup)
    gpt_server.start()

def gptStop():
    if 'gpt_server' in globals():
        gpt_server.terminate()
