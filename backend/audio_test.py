import uuid
from audio import audioAddAlaw, audioEnd, audioAddPCM16

uuid = str(uuid.uuid4())

with open("audio.data", 'r') as file:
    global audio
    audio = file.read()

audioAddPCM16({
    "uuid": uuid,
    "audio": audio
})
print(audioEnd({
    "uuid": uuid}))