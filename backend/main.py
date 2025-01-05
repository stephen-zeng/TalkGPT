from gevent import monkey
monkey.patch_all()

from django.core.management import call_command
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talkgpt.settings')
django.setup()

from geventwebsocket.handler import WebSocketHandler
import threading
from core.models import Conversation
from core.serializer import ConversationSerializer
from core.signals import modelSignal
from core.methods import modelNewConversation, modelDelConversation, modelEditConversation
from core.methods import modelNewMemory, modelDelMemory
from gpt import gptInit, gptConnect, gptDisconnect, gptSignal
from gpt import gptNewConversation, gptUpdateConversation
from gpt import gptNewMemory, gptDelMemory
from gpt import gptNewVoice, gptAddVoice, gptCancelVoice, gptSendVoice
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
            uuid = modelNewConversation(data)
            data['uuid'] = uuid
            gptNewConversation(data)
        case 'delConversation':
            modelDelConversation(data)
        case 'editConversation':
            modelEditConversation(data)
            gptUpdateConversation(data)
        case 'newMemory':
            uuid = modelNewMemory(data)['uuid']
            data['uuid'] = uuid
            gptNewMemory(data)
        case 'delMemory':
            id = modelDelMemory(data)
            data['serverid'] = id['serverid']
            data['uuid'] = id['uuid']
            gptDelMemory(data)
        case _:
            print(f"From {sid}, receive an unknown operation")

@gptSignal.connect
@sio.event
def openai(sid, operation, data):
    match operation:
        case 'setConfig': # 来自前端
            print(f"From {sid}, set the config")
            print(data)
            global api_key
            api_key = data['key']
            gptInit(key=api_key)
        case 'connect': # 来自前端
            if api_key == 'None':
                sio.emit('openai_response', 'unConfigured')
                return
            gptConnect()
        case 'disconnect': # 来自前端
            gptDisconnect()
        case 'newVoice':
            gptNewVoice(data)
        case 'addVoice':
            gptAddVoice(data)
        case 'sendVoice':
            gptSendVoice()
        case 'cancelVoice':
            gptCancelVoice()
        case 'connected': # 来自gpt
            sio.emit('openai_response', 'connected')
        case 'disconnected': # 来自gpt
            sio.emit('openai_response', 'disconnected')
        case 'replied': # 来自gpt
            sio.emit('openai_response', 'replied')
            

def init(port):
    print(f"The server from port {port} is up and running.")
    server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', port),
        app,
        handler_class=WebSocketHandler 
    )
    server.serve_forever()

def djangoRun(port):
    call_command('runserver', port)

if __name__ == '__main__':
    main = threading.Thread(target=init, args=(11111,))
    download = threading.Thread(target=djangoRun, args=('8080',))
    main.start()
    download.start()
    main.join()
    download.join()
    gptDisconnect()
