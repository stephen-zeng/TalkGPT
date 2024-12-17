from django.db import models
import uuid

class Conversation(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    vad_free = models.BooleanField(default=True)
    vad_url = models.TextField()
    manual_free = models.BooleanField(default=True)
    voice = models.CharField(max_length=7)
    instruction = models.TextField()
    time = models.DateTimeField(auto_now=True)

class Manual(models.Model):
    conversation = models.ForeignKey("Conversation",
                                     on_delete=models.CASCADE,
                                     related_name="manual",
                                     null=True)
    role = models.BooleanField()
    message = models.TextField()
    voice = models.URLField()
    time = models.DateTimeField(auto_now=True)

class VAD(models.Model):
    conversation = models.ForeignKey("Conversation",
                                     on_delete=models.CASCADE,
                                     related_name="vad",
                                     null=True)
    role = models.BooleanField()
    message = models.TextField()
    voice = models.URLField()
    time = models.DateTimeField(auto_now=True)
    


# Create your models here.