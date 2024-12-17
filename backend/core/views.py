from rest_framework import viewsets
from .models import Conversation
from .serializer import ConversationSerializer

class ConversationViewset(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('time')
    serializer_class = ConversationSerializer
