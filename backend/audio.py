import base64
import wave
import os
import numpy as np
import socketio
from pydub import AudioSegment

global path
global audio
audio = {}

def audioAdd(data):
    uuid = str(data['uuid'])
    path = f'audio/{uuid}.wav'
    global audio
    try:
        chunk = base64.b64decode(data['audio'])
    except Exception as e:
        print(f"Decoding error: {e}")
        return None

    if uuid in audio:
        audio[uuid] += chunk
    else:
        audio[uuid] = chunk
    
    return f'https://talk.goforit.top/download/{path}'


def audioDel(data):
    path = 'audio/' + str(data['uuid']) + '.wav'
    try:
        os.remove(path)
    except FileNotFoundError:
        print(f"File {path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def audioEnd(data):
    print("Here comes the audio ending")
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
    except Exception as e:
        print(f"Error when saving audio: {e}")
        return None

    del audio[uuid]
    return f'https://talk.goforit.top/download/{path}'

def audioSend(data):
    path = 'audio/' + str(data['uuid']) + '.wav'
    audio = AudioSegment.from_wav(path)
    audio = audio.set_frame_rate(24000).set_channels(1)
    chunks = make_chunks(audio, 100)

    for i, chunk in enumerate(chunks):
        pcm_data = np.array(chunk.get_array_of_samples())
        pcm_base64 = base64.b64encode(pcm_data.tobytes()).decode('utf-8')
        chunks[i] = pcm_base64
    return chunks

def make_chunks(audio_segment, chunk_length_ms):
    chunk_length = chunk_length_ms * audio_segment.frame_rate // 100
    return [audio_segment[i:i + chunk_length] for i in range(0, len(audio_segment), chunk_length)]

        
    