import base64
import wave
import audioop
import os

global path
global audio
audio = {}

def audioAdd(data):
    print("Here comes an audio data")
    print(data)
    uuid = str(data['uuid'])
    path = f'audio/{uuid}.wav'
    global audio
    # 解码 Base64 数据
    try:
        chunk = base64.b64decode(data['audio'])
    except Exception as e:
        print(f"Base64 解码失败: {e}")
        return None

    if uuid in audio:
        audio[uuid] += chunk
    else:
        audio[uuid] = chunk
    
    return f'https://talk.goforit.top/{path}'


def audioDel(data):
    path = 'audio/' + str(data['uuid']) + '.wav'
    try:
        os.remove(path)
        print(f"File {path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def audioEnd(data):
    print("Here comes the audio ending")
    print(data)
    global audio
    uuid = str(data['uuid'])

    if uuid not in audio:
        print(f"No audio data found for UUID {uuid}")
        return None

    pcm16 = audio[uuid]
    path = f'audio/{uuid}.wav'

    try:
        with wave.open(path, 'wb') as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(24000)
            file.writeframes(pcm16)
        print(f"WAV 文件已保存: {path}")
    except Exception as e:
        print(f"保存 WAV 文件时出错: {e}")
        return None

    del audio[uuid]
    return f'https://talk.goforit.top/{path}'

        
    