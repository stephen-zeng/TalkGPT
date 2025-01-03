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
from core.methods import addConversation, addText, addVoice
from core.methods import delConversation, delTalking
from gpt import gptInit, gptConnect, gptDisconnect, gptSignal
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
            print(f"From {sid}, add a new Conversation")
            addConversation(data)
        case 'newText':
            print(f"From {sid}, a new text message")
            addText(data)
        case 'newVoice':
            print(f"From {sid}, a new voice message")
            addVoice(data)
        case 'deleteConversation':
            print(f'From {sid}, delete a conversation')
            delConversation(data)
        case 'deleteTalking':
            print(f"From {sid}, delete a talking")
            delTalking(data)
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
            global gpt_model
            api_key = data['key']
            gpt_model = data['model']
            gptInit(key=api_key, model=gpt_model)
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
