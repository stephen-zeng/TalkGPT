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
from core.methods import modelNewConversation, modelDelConversation, modelEditConversation
from core.methods import modelNewMemory, modelDelMemory
from gpt import gptInit, gptConnect, gptDisconnect, gptSignal
from gpt import gptNewConversation, gptUpdateConversation
from gpt import gptNewMemory, gptDelMemory, gptRequire
from gpt import gptNewVoice, gptAddVoice, gptCancelVoice, gptSendVoice
from audio import audioDel, audioSend
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
            memories = modelDelConversation(data)
            for uuid in memories:
                audioDel({'uuid': uuid})
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
        case 'requireAudio':
            sio.emit('backend', 'processing')
            sio.emit('audio', {
                "type": 'newAudio'
            })
            for chunk in audioSend(data):
                sio.emit('audio', {
                    'type': 'addAudio',
                    'audio': chunk
                })
            sio.emit('backend', 'processed')
        
        case _:
            print(f"From {sid}, receive an unknown operation")

@gptSignal.connect
@sio.event
def openai(sid, operation, data):
    match operation:
        case 'setConfig': # 来自前端
            print(f"From {sid}, set the config")
            global api_key
            api_key = data['key']
            gptInit(key=api_key)
        case 'connect': # 来自前端
            if api_key == 'None':
                sio.emit('openai_response', 'unConfigured')
                return
            gptConnect()
        case 'change':
            gptUpdateConversation(data)
        case 'disconnect': # 来自前端
            gptDisconnect()
        case 'newVoice':
            gptNewVoice()
        case 'addVoice':
            gptAddVoice(data)
        case 'sendVoice':
            gptSendVoice()
        case 'cancelVoice':
            gptCancelVoice()
        case 'reply':
            gptRequire()
        case 'connected': # 来自gpt
            sio.emit('openai_response', 'connected')
            # sio.emit('backend', 'processed')
        case 'disconnected': # 来自gpt
            sio.emit('openai_response', 'disconnected')
            # sio.emit('backend', 'processed')
        case 'inited':
            sio.emit('openai_response', 'inited')
        case 'replying':# 来自gpt
            sio.emit('backend', 'processing')
        case 'replied': # 来自gpt
            sio.emit('backend', 'processed')
        case 'newAudio': # 来自gpt
            sio.emit('audio', {
                "type": 'newAudio'
            })
        case 'addAudio': # 来自gpt
            sio.emit('audio', {
                'type': 'addAudio',
                'audio': data['audio']
            })

            

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
