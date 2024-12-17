from django.contrib import admin
from .models import Conversation, Manual, VAD

admin.site.register(Conversation)
admin.site.register(Manual)
admin.site.register(VAD)

# Register your models here.
