from django.db.models.signals import post_save, post_migrate, post_delete, post_init
from django.dispatch import receiver
from core.models import Conversation, Manual, VAD
from core.sio import send_data

@receiver(post_save, sender=Conversation)
def model_save(**kwargs):
    print("Model Save")
    send_data()

@receiver(post_migrate, sender=Conversation)
def model_save(**kwargs):
    print("Model Save")
    send_data()

@receiver(post_delete, sender=Conversation)
def model_save(**kwargs):
    print("Model Save")
    send_data()

@receiver(post_init, sender=Conversation)
def model_save(**kwargs):
    print("Model Save")
    send_data()
