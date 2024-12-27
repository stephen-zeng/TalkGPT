import socketio
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('get_data')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def data_response(data):
    print('Received data:')
    print(data)

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:11111')
    sio.emit('write_data')
    sio.wait()
