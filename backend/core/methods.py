from core.models import Conversation, Memory
import json

def newConversation(data):
    print("Receive new Conversation!")
    # print(type(data))
    print(data)
    # data = json.loads(data)
    # print(data['title'])
    new = Conversation(
        title = data['title'],
        model = data['model'],
        temperature = data['temperature'],
        instruction = data['instruction'],
        voice = data['voice'],
        vad = data['vad'],
    )
    new.save()
    return new.uuid

def delConversation(data):
    print("Delete a conversation")
    print(data)
    Conversation.objects.get(uuid=data['uuid']).delete()

def editConversation(data):
    print("Edit a conversation")
    print(data)
    edit = Conversation.objects.get(uuid=data['uuid'])
    edit.title = data['title']
    edit.model = data['model']
    edit.temperature = data['temperature']
    edit.instruction = data['instruction']
    edit.save()

def newMemory(data):
    print("Receive new message")
    print(data)
    new = Memory(
        role = data['role'],
        message = data['message'],
        voice = data['voice'],
        conversation = Conversation.objects.get(uuid=data['uuid'])
    )
    new.save()
    return new.uuid

def editMemory(data):
    edit = Memory.objects.get(uuid=data['uuid'])
    if (data['text']):
        edit.message = data['text']
    if (data['voice']):
        edit.voice = data['voice']
    edit.save()

def delMemory(data):
    print("Delete a talking")
    print(data)
    Memory.objects.get(uuid=data['uuid']).delete()

def addVoiceTranscription(uuid, text):
    edit = Memory.objects.get(uuid = uuid)
    edit.message = text
    edit.save()
    return edit.uuid

def newGPTMemory(id, uuid):
    new = Memory(
        role = True,
        serverID = id,
        conversation = Conversation.objects.get(uuid=uuid)
    )
    new.save()
    return new.uuid
    