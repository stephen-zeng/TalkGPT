from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Conversation, Memory
from blinker import signal

modelSignal = signal('modelSignal')

@receiver(post_save, sender=Memory)
@receiver(post_save, sender=Conversation)
@receiver(post_delete, sender=Memory)
@receiver(post_delete, sender=Conversation)
def model_save(**kwargs):
    modelSignal.send(0, operation='data', data=0)
