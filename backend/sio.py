from gevent import monkey
monkey.patch_all()

import gevent.pywsgi
from geventwebsocket.handler import WebSocketHandler  # 注意这里
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

# 使用 Gevent 异步模式
sio = socketio.Server(
    cors_allowed_origins='*',
    async_mode='gevent'
)
app = socketio.WSGIApp(sio)

# 定义 Socket.IO 事件
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

@sio.event
def write_data(sid):
    print("Writing Data")
    Conversation.objects.create(
        title = "test",
        vad_free = True,
        vad_url = "aaaaaaa",
        manual_free = False,
        voice = "test",
        instruction = "asdasdjlhhjlkashjlkdahljkas",    
    )

def send_data(_, **kwargs):
    print("Sending data to all clients")
    queryset = Conversation.objects.all().order_by('time')
    serializer = ConversationSerializer(queryset, many=True)
    sio.emit('data_response', json.dumps(serializer.data))


# 连接信号
dSignal.connect(send_data)

print("Server is running...")

if __name__ == '__main__':
    # 配置 Gevent WSGI 服务器，使用 WebSocketHandler
    server = gevent.pywsgi.WSGIServer(
        ('127.0.0.1', 11111),
        app,
        handler_class=WebSocketHandler  # 关键配置
    )
    server.serve_forever()
