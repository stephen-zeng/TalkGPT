import base64
import wave
import audioop
import os

global path

def audioAddPCM16(data):
    path = 'audio/' + data['uuid'] + '.wav'
    if (os.path.exists(path) == False):
        return
    pcm16 = base64.b64decode(data['audio'])
    with wave.open(path, 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(44100)
        audio.writeframes(pcm16)
    return 'https://talk.goforit.top/' + path

def audioAddAlaw(data):
    path = 'audio/' + data['uuid'] + '.wav'
    alaw = base64.b64decode(data['audio'])
    pcm16 = audioop.alaw2lin(alaw, 2)
    with wave.open(path, 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(44100)
        audio.writeframes(pcm16)
    return 'https://talk.goforit.top/' + path

def audioDel(data):
    path = 'audio/' + data['uuid'] + '.wav'
    try:
        os.remove(path)
        print(f"File {path} deleted successfully.")
    except FileNotFoundError:
        print(f"File {path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def audioEnd(data):
    path = 'audio/' + data['uuid'] + '.wav'
    return 'https://talk.goforit.top/' + path
        
    