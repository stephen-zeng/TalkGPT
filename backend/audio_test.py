import uuid
from audio import audioAddAlaw, audioEnd

uuid = str(uuid.uuid4())

with open("audio.data", 'r') as file:
    global audio
    audio = file.read()

audioAddAlaw({
    "uuid": uuid,
    "audio": audio
})
print(audioEnd({
    "uuid": uuid}))