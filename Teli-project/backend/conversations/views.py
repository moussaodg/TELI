from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .services import ConversationService
from accounts.models import Administrator, role


class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def view_conversation(self, request, channel_user_id):
        try:
            conversation = ConversationService.get_conversation_by_channel_user(channel_user_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        messages = Message.objects.filter(conversation=conversation)
        conversation_serializer = ConversationSerializer(conversation)
        message_serializer = MessageSerializer(messages, many=True)
        return Response({
            'conversation': conversation_serializer.data,
            'messages': message_serializer.data
        }, status=200)
    
    def view_single_message(self, request, message_id):
        try:
            message = ConversationService.get_message(message_id)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)
        
        message_serializer = MessageSerializer(message)
        return Response(message_serializer.data, status=200)
    
    def list_conversations(self, request):
        conversations = ConversationService.list_conversations()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=200)
    
    def list_messages(self, request):
        messages = ConversationService.list_messages()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)
    
    def modify_message(self, request, message_id):
        try:
            message = ConversationService.get_message(message_id)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)
        
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def close_conversation(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        ConversationService.close_conversation(conversation)
        return Response({'message': 'Conversation closed successfully'}, status=200)
    
    def reopen_conversation(self, request, channel_user_id):
        try:
            conversation = ConversationService.get_conversation_by_channel_user(channel_user_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        ConversationService.reopen_conversation(conversation)
        return Response({'message': 'Conversation reopened successfully'}, status=200)
    
    def delete_message(self, request, message_id):
        try:
            message = ConversationService.get_message(message_id)
            ConversationService.delete_message(message)
            return Response({'message': 'Message deleted successfully'}, status=200)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)


class ConversationManagementViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def prendre_en_charge_conversation(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        
        if conversation.administrator is not None:
            return Response({'message': 'Conversation already taken in charge'}, status=400)
        try:
            administrator = request.user.administrator
        except AttributeError:
            return Response({'message': 'Authenticated user is not an administrator'}, status=403)
        ConversationService.assign_conversation(conversation, administrator)
        return Response({'message': 'Conversation taken in charge successfully'}, status=200)
