import socketio

# 创建 Socket.IO 客户端
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('get_data')  # 请求数据

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def data_response(data):
    print('Received data:')
    print(data)

if __name__ == '__main__':
    # 连接到 Socket.IO 服务器
    sio.connect('http://127.0.0.1:11111')
    # 保持连接
    sio.wait()
