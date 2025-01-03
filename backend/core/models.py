from django.db import models
import uuid

class Conversation(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False,
                            unique=True)
    time = models.DateTimeField(auto_now=True)
    model = models.TextField(null=True)
    voice = models.CharField(max_length=7)
    temperature = models.DecimalField(max_digits=2, 
                                      decimal_places=1,
                                      null=True) # 0.6~1.2
    instruction = models.TextField(null=True)
    vad = models.BooleanField(default=False)

class Memory(models.Model):
    conversation = models.ForeignKey("Conversation",
                                     on_delete=models.CASCADE,
                                     related_name="memory",
                                     null=True)
    role = models.BooleanField(default=False)
    message = models.TextField(null=True)
    voice = models.TextField(null=True) # This is the voice wav link
    time = models.DateTimeField(auto_now=True)
    serverID = models.TextField(null=True)
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False,
                            unique=True)
    


# Create your models here.
