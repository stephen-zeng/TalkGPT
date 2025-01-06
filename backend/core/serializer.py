from rest_framework import serializers
from .models import Conversation, Memory

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = [
            "role",
            "message",
            "voice",
            "time",
            "uuid",
            "serverid",
        ]

class ConversationSerializer(serializers.ModelSerializer):
    memory = MemorySerializer(many=True)

    class Meta:
        model = Conversation
        fields = [
            "title",
            "uuid",
            "time",
            "memory",
            "model",
            "voice",
            "temperature",
            "instruction",
            "vad",
            "key"
        ]
