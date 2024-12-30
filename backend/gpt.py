from concurrent.futures import ThreadPoolExecutor
import os
import json
import websocket
import threading
import time

def on_open(ws):
    print("Connected to OpenAI")

def on_message(ws, data):
    print("Receive data from OpenAI")
    print(data)

with ThreadPoolExecutor(max_workers=2) as executor:
    def start():
        ws.run_forever()
    def gptStop():
        print("Try to close connection to the OpenAI")
        try:
            ws.close()
            print("Closed")
        except:
            print("The connection isn't alive")
    def gptStart():
        gptStop()
        print("Establishing the connection to OpenAI")
        executor.submit(start)

    

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
    global server
    server = threading.Thread(target=start)
