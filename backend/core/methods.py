from core.models import Conversation, Manual, VAD
import json

def addConversation(data):
    print("Receive new Conversation!")
    # print(type(data))
    print(data)
    # data = json.loads(data)
    # print(data['title'])
    Conversation.objects.create(
        title = data['title'],
        instruction = data['instruction'],
        voice = data['voice']
    )

def addText(data):
    print("Receive new text message")
    print(data)
    Manual.objects.create(
        role = False,
        message = data['message'],
        conversation = Conversation.objects.get(uuid=data['uuid'])
    )

def addVoice(data):
    print("Receive new voice message")
    print(data)
    Manual.objects.create(
        role = False,
        message = "Should be from the wisper",
        voice = data['voice'],
        conversation = Conversation.objects.get(uuid=data['uuid'])
    )

def delConversation(data):
    print("Delete a conversation")
    print(data)
    Conversation.objects.get(uuid=data['uuid']).delete()

def delTalking(data):
    print("Delete a talking")
    print(data)
    try:
        Manual.objects.get(time=data['time']).delete()
    except:
        VAD.objects.get(time=data['time']).delete()