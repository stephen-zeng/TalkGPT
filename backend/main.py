from gevent import monkey
monkey.patch_all()

import gevent.pywsgi
from geventwebsocket.handler import WebSocketHandler
from multiprocessing import Process
import socketio
import django
import json
import os

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talkgpt.settings')
django.setup()

from core.models import Conversation
from core.serializer import ConversationSerializer
from core.signals import dSignal
from core.methods import addConversation, addText, addVoice
from core.methods import delConversation, delTalking
from gpt import gptInit, gptStop

sio = socketio.Server(
    cors_allowed_origins='*',
    async_mode='gevent'
)
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)

@sio.event
def get_data(sid):
    print("Client requested data")
    queryset = Conversation.objects.all().order_by('time')
    serializer = ConversationSerializer(queryset, many=True)
    sio.emit('data_response', json.dumps(serializer.data), room=sid)

def send_data(_, **kwargs):
    print("Sending data to all clients")
    queryset = Conversation.objects.all().order_by('time')
    serializer = ConversationSerializer(queryset, many=True)
    sio.emit('data_response', json.dumps(serializer.data))

@sio.event
def setConfig(sid, data):
    print(f"From {sid}, set the config")
    print(data)
    global api_key
    global gpt_model
    api_key = data['key']
    gpt_model = data['model']

@sio.event
def startConversation(sid):
    print(f"From {sid}, start the conversation")
    gptStop()
    gptInit(api_key, gpt_model)

@sio.event
def stopConversation(sid):
    print(f"From {sid}, stop the conversation")
    gptStop()

@sio.event
def newConversation(sid, data):
    print(f"From {sid}, add a new Conversation")
    addConversation(data)

@sio.event
def newText(sid, data):
    print(f"From {sid}, a new text message")
    addText(data)

@sio.event
def newVoice(sid, data):
    print(f"From {sid}, a new voice message")
    addVoice(data)

@sio.event
def deleteConversation(sid, data):
    print(f'From {sid}, delete a conversation')
    delConversation(data)
    gptStop()

@sio.event
def deleteTalking(sid, data):
    print(f"From {sid}, delete a talking")
    delTalking(data)


dSignal.connect(send_data)

def init():
    server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', 11111),
        app,
        handler_class=WebSocketHandler 
    )
    server.serve_forever()


if __name__ == '__main__':
    main = Process(target=init)
    main.start()
    print("The Main Server is running")
    main.join()
