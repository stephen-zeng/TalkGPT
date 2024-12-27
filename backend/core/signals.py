from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Conversation, Manual, VAD
from blinker import signal

dSignal = signal('modelChanged')

@receiver(post_save, sender=VAD)
@receiver(post_save, sender=Manual)
@receiver(post_save, sender=Conversation)
def model_save(**kwargs):
    print("Model Save")
    dSignal.send()
