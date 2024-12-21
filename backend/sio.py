import eventlet.wsgi
import socketio
import eventlet
import django
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'talkgpt.settings')
django.setup()

from core.models import Conversation
from core.serializer import ConversationSerializer

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# sid是Client的ID
@sio.event
def connect(sid, _):
    print("Client connect", sid)

@sio.event
def disconnect(sid):
    print("Client disconnected", sid)

@sio.event
def get_data(sid):
    print("Client Require Data")
    queryset = Conversation.objects.all().order_by('time')
    serializer = ConversationSerializer(queryset, many=True)
    sio.emit('data_response', json.dumps(serializer.data), room=sid)

def send_data():
    print("Send data to all the Client")
    queryset = Conversation.objects.all().order_by('time')
    serializer = ConversationSerializer(queryset, many=True)
    sio.emit('data_response', json.dumps(serializer.data))


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 11111)), app)
