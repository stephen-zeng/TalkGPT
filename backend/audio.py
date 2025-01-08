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
    path = 'audio/' + str(data['uuid']) + '.wav'
    global audio
    if str(data['uuid']) in audio:
        audio[str(data['uuid'])] += data['audio']
    else:
        audio[str(data['uuid'])] = data['audio']
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
    print("Here comes the audio ending")
    print(data)
    global audio
    print(audio[str(data['uuid'])])
    path = 'audio/' + str(data['uuid']) + '.wav'
    if data['frame']==24000:
        pcm16 = base64.b64decode(audio[str(data['uuid'])])
    else:
        alaw = base64.b64decode(audio[str(data['uuid'])])
        pcm16 = audioop.alaw2lin(alaw, 2)
    with wave.open(path, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(data['frame'])
        file.writeframes(pcm16)
    del audio[str(data['uuid'])]
    return 'https://talk.goforit.top/' + path
        
    