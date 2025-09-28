from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve and create conversations.
    POST /conversations/ with {"participants": [user_ids]} creates a conversation.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom create to attach participants.
        Expects a JSON body: {"participants": [<uuid>, <uuid>, ...]}
        The requesting user is automatically included if not listed.
        """
        participant_ids = self.request.data.get("participants", [])
        participants = list(User.objects.filter(user_id__in=participant_ids))

        # Ensure the creator is included
        if self.request.user not in participants:
            participants.append(self.request.user)

        conversation = serializer.save()
        conversation.participants.set(participants)
        conversation.save()

    def create(self, request, *args, **kwargs):
        """
        Override to accept participants and return full nested data.
        """
        serializer = self.get_serializer(data={})  # No direct fields, participants handled separately
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            ConversationSerializer(serializer.instance, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and create messages.
    POST /messages/ with {"conversation": <uuid>, "message_body": "..."}
    sends a message to that conversation.
    """
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically sets the sender to the authenticated user.
        """
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        """
        Optionally filter by conversation using ?conversation=<uuid>
        """
        queryset = super().get_queryset()
        conv_id = self.request.query_params.get("conversation")
        if conv_id:
            queryset = queryset.filter(conversation__conversation_id=conv_id)
        return queryset
