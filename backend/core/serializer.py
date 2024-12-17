from rest_framework import serializers
from .models import Conversation, Manual, VAD

class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = [
            'role',
            'message',
            'voice',
            'time'    
        ]

class VADSerializer(serializers.ModelSerializer):
    class Meta:
        model = VAD
        fields = [
            'role',
            'message',
            'voice',
            'time'    
        ]

class ConversationSerializer(serializers.ModelSerializer):
    manual = ManualSerializer(many=True)
    vad = VADSerializer(many=True)

    class Meta:
        model = Conversation
        fields = [
            'title',
            'uuid',
            'vad_free',
            'vad_url',
            'manual_free',
            'voice',
            'instruction',
            'time',
            'manual',
            'vad',
        ]
