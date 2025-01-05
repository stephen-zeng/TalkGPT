from core.models import Conversation, Memory
import json

def modelNewConversation(data):
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
    edit = Conversation.objects.get(uuid = data['uuid'])
    edit.title = data['title']
    edit.model = data['model']
    edit.instruction = data['instruction']
    edit.vad = data['vad']
    edit.temperature = data['temperature']
    edit.save()

def modelDelConversation(data):
    delete = Conversation.objects.get(uuid=data['uuid'])
    delete.delete()

def modelNewMemory(data):
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
    delete = Memory.objects.get(uuid=data['uuid'])
    serverid = delete.serverid
    uuid = delete.uuid
    delete.delete()
    return {
        'uuid': uuid,
        'serverid': serverid
    }

def modelEditMemory(data):
    if (data['uuid']!='None'): # 给啥用啥
        edit = Memory.objects.get(uuid=data['uuid'])
    else:
        edit = Memory.objects.get(serverid=data['serverid'])
    if (data['message']!='None'):
        edit.message = data['message']
    if (data['voice']!='None'):
        edit.voice = data['voice']
    edit.save()
    return {
        'uuid': edit.uuid,
        'serverid': edit.serverid
    }