import uuid
from audio import audioAdd, audioEnd

uuid = str(uuid.uuid4())

with open("audio.data", 'r') as file:
    global audio
    audio = file.read()

audioAdd({
    "uuid": uuid,
    "audio": audio
})
print(audioEnd({
    "uuid": uuid}))