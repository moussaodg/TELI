from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import IsSuperAdmin

from .models import RasaClient
from conversations.models import Conversation
from .serializers import RasaClientSerializer
from .services import RasaClientService
 


class RasaClientViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def send_message(self, request):
        channel = request.data.get('channel')
        channel_user_id = request.data.get('channel_user_id')
        message_text = request.data.get('message')

        if not channel or not channel_user_id or not message_text:
            return Response(
                {'error': 'channel, channel_user_id and message are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rasa_client = RasaClientService.get_or_create_client(channel, channel_user_id)
        conversation = rasa_client.ConversationId

        client_actor = RasaClientService.get_or_create_client_actor(rasa_client)
        user_message = RasaClientService.create_user_message(conversation, client_actor, message_text)

        try:
            rasa_data = RasaClientService.send_to_rasa(channel_user_id, message_text)
        except Exception:
            return Response(
                {'error': 'Rasa server unreachable'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        bot_actor = RasaClientService.get_or_create_bot_actor()
        bot_messages = RasaClientService.create_bot_messages(conversation, bot_actor, user_message, rasa_data)
        RasaClientService.create_notifications_for_messages(bot_messages)

        return Response({
            'conversation_id': conversation.id,
            'user_message': message_text,
            'bot_responses': [msg.content for msg in bot_messages],
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def ask_administrator_intervention(self, request):
        channel_user_id = request.data.get('channel_user_id')
        message_text = request.data.get('message')
        channel = request.data.get('channel', 'facebook')

        if not channel_user_id or not message_text:
            return Response(
                {'error': 'channel_user_id and message are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rasa_client, created = RasaClient.objects.get_or_create(
            Channel=channel,
            ChannelUserId=channel_user_id,
            defaults={'ConversationId': Conversation.objects.create()}
        )

        conversation = rasa_client.ConversationId
        client_actor = RasaClientService.get_or_create_client_actor(rasa_client)
        user_message = RasaClientService.create_user_message(conversation, client_actor, message_text)
        bot_message = RasaClientService.create_administrator_intervention_request(conversation, user_message)

        return Response({
            'message': 'Administrator intervention requested successfully. Un administrateur va prendre en charge votre demande, veuillez patienter.',
            'bot_response': bot_message.content,
        }, status=status.HTTP_200_OK)


    def create(self, request):
        return self.send_message(request)


class RasaClientManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def list(self, request):
        rasa_clients = RasaClient.objects.all()
        serializer = RasaClientSerializer(rasa_clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            rasa_client = RasaClient.objects.get(pk=pk)
        except RasaClient.DoesNotExist:
            return Response({'message': 'RasaClient not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RasaClientSerializer(rasa_client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    