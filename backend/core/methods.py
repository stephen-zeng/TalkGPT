from core.models import Conversation, Memory
import json

def modelNewConversation(data):
    print('modelNewConversation')
    print(data)
    new = Conversation(
        title = data['title'],
        model = data['model'],
        voice = data['voice'],
        temperature = data['temperature'],
        instruction = data['instruction'],
        vad = data['vad'],
    )
    new.save()
    return new.uuid

def modelEditConversation(data):
    print('modelEditConversation')
    print(data)
    edit = Conversation.objects.get(uuid = data['uuid'])
    print(f"found {edit}")
    if 'title' in data:
        edit.title = data['title']
    if 'model' in data:
        edit.model = data['model']
    if 'instruction' in data:
        edit.instruction = data['instruction']
    if 'vad' in data:
        edit.vad = data['vad']
    if 'temperature' in data:
        edit.temperature = data['temperature']
    if 'key' in data:
        edit.key = data['key']
    print(f"edited {edit}")
    edit.save()

def modelDelConversation(data):
    print('modelDelConversation')
    print(data)
    delete = Conversation.objects.get(uuid=data['uuid'])
    delete.delete()

def modelNewMemory(data):
    print('modelNewMemory')
    print(data)
    new = Memory(
        message = data['message'],
        voice = data['voice'],
        role = data['role'],
        serverid = data['serverid'],
        conversation = Conversation.objects.get(uuid=data['uuid']),
    )
    new.save()
    return {
        'uuid': new.uuid,
        'serverid': new.serverid,
    }
    
def modelDelMemory(data):
    print('modelDelMemory')
    print(data)
    delete = Memory.objects.get(uuid=data['uuid'])
    serverid = delete.serverid
    uuid = delete.uuid
    delete.delete()
    return {
        'uuid': uuid,
        'serverid': serverid
    }

def modelEditMemory(data): # 主要是更改transcription，所以是加法
    print('modelEditMemory')
    print(data)
    if 'uuid' in data:
        print('Find by UUID')
        edit = Memory.objects.get(uuid=data['uuid'])
    elif 'serverid' in data:
        print('Find by serverid')
        edit = Memory.objects.get(serverid=data['serverid'])
    else:
        print("Unable to find")
        return
    print(f"found {edit}")
    if 'message' in data:
        if edit.message == "Waiting for transcription":
            edit.message = ''
        edit.message += data['message']
    if 'voice' in data:
        edit.voice = data['voice']
    if 'serverid' in data:
        edit.serverid = data['serverod']
    print(f"edited serverID {edit.serverid}")
    edit.save()
    print(f"saved serverID {edit.serverid}")
    return {
        'uuid': edit.uuid,
        'serverid': edit.serverid
    }