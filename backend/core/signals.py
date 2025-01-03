from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Conversation, Manual, VAD
from blinker import signal

modelSignal = signal('modelSignal')

@receiver(post_save, sender=VAD)
@receiver(post_save, sender=Manual)
@receiver(post_save, sender=Conversation)
@receiver(post_delete, sender=VAD)
@receiver(post_delete, sender=Manual)
@receiver(post_delete, sender=Conversation)
def model_save(**kwargs):
    print("Model Changed")
    modelSignal.send(0, operation='data', data=0)
