from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.models import Administrator, role
from noifications.models import Notification


class ConversationViewSet(viewsets.ViewSet):

    def view_conversation(self, request, ChannelUserId):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        try:
            conversation = Conversation.objects.get(rasa_clients__ChannelUserId=ChannelUserId)
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
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)
        
        message_serializer = MessageSerializer(message)
        return Response(message_serializer.data, status=200)
    
    def list_conversations(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=200)
    
    def list_messages(self, request):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=200)
    
    def modify_message(self, request, message_id):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)
        
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def close_conversation(self, request, conversation_id):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        
        conversation.is_satisfied = True
        conversation.save()
        return Response({'message': 'Conversation closed successfully'}, status=200)
    
    def reopen_conversation(self, request, ChannelUserId):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            conversation = Conversation.objects.get(rasaclient__ChannelUserId=ChannelUserId)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        
        conversation.is_satisfied = False
        conversation.save()
        return Response({'message': 'Conversation reopened successfully'}, status=200)
    
    def delete_message(self, request, message_id):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return Response({'message': 'Message deleted successfully'}, status=200)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=404)


class CoversationManagementViewset(viewsets.ViewSet):

    def prendre_en_charge_conversation(self, request, conversation_id):
        if not request.user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=401)
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'message': 'Conversation not found'}, status=404)
        
        if conversation.administrator is not None:
            return Response({'message': 'Conversation already taken in charge'}, status=400)
        
        conversation.administrator = request.user.administrator
        conversation.save()
        return Response({'message': 'Conversation taken in charge successfully'}, status=200)
