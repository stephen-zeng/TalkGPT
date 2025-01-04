from gevent import monkey
monkey.patch_all()

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talkgpt.settings')
django.setup()

from geventwebsocket.handler import WebSocketHandler
import threading
from core.models import Conversation
from core.serializer import ConversationSerializer
from core.signals import modelSignal
# from core.methods import modelNewConversation, modelEditConversation, modelDelConversation
# from core.methods import modelNewMemory, modelDelMemory
from gpt import gptInit, gptConnect, gptDisconnect, gptSignal
# from gpt import gptNewConversation, gptEditConversation
# from gpt import gptNewMemory, gptDelMemory
import gevent.pywsgi
import socketio
import django
import json

sio = socketio.Server(
    cors_allowed_origins='*',
    async_mode='gevent'
)
app = socketio.WSGIApp(sio)
api_key = 'None'
gpt_model = 'None'

@sio.event
def connect(sid, _):
    print("Client connected:", sid)

@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)
    gptDisconnect()

@modelSignal.connect
@sio.event
def model(sid, operation, data):
    match operation:
        case 'data':
            print("Sending data")
            queryset = Conversation.objects.all().order_by('time')
            serializer = ConversationSerializer(queryset, many=True)
            if sid == 0:
                sio.emit('data_response', json.dumps(serializer.data))
            else:
                 sio.emit('data_response', json.dumps(serializer.data), room=sid)
        case 'newConversation':
            
        case 'delConversation':
            
        case 'editConversation':
            
        case 'newMemoryText':

        case 'delMemory':
            
        case _:
            print(f"From {sid}, receive an unknown operation")

@gptSignal.connect
@sio.event
def openai(sid, operation, data):
    match operation:
        case 'setConfig':
            print(f"From {sid}, set the config")
            print(data)
            global api_key
            api_key = data['key']
            gptInit(key=api_key)
        case 'connect':
            if api_key == 'None':
                sio.emit('openai_response', 'unConfigured')
                return
            gptConnect()
        case 'disconnect':
            gptDisconnect()
        case 'connected':
            sio.emit('openai_response', 'connected')
        case 'disconnected':
            sio.emit('openai_response', 'disconnected')
            

def init(port):
    print(f"The server from port {port} is up and running.")
    server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', port),
        app,
        handler_class=WebSocketHandler 
    )
    server.serve_forever()


if __name__ == '__main__':
    main = threading.Thread(target=init, args=(11111,))
    main.start()
    main.join()
    gptDisconnect()
