from django.shortcuts import render
from .models import RasaClient
from conversations.models import Message, Conversation, Actor
from .serializers import RasaClientSerializer
from conversations.serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.models import Administrator, role
from rest_framework import viewsets
from rest_framework import status
from notifications.models import Notification



class RasaClientViewSet(viewsets.ViewSet):

    def get_conversation_context(self, conversation):
        conversation = Conversation.objects.get(id=conversation.id)
        get_messages = Message.objects.filter(conversation=conversation).last()
        try:
            rasa_context_generator = requets.get(f"http://chatbot:5005/conversations/{conversation.id}/tracker")
            rasa_context = rasa_context_generator.json()
            return rasa_context
        except Exception:
            return None

    @action(detail=False, methods=['post'])
    def send_message(self, request):

    # =========================
    # 1. RÉCUPÉRATION DONNÉES
    # =========================
        channel = request.data.get('channel')
        channel_user_id = request.data.get('channel_user_id')
        message_text = request.data.get('message')

        if not channel or not channel_user_id or not message_text:
            return Response(
                {'error': 'channel, channel_user_id and message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ===========================================
        # 2. GET OR CREATE CLIENT + CONVERSATION
        # ===========================================
        rasa_client, created = RasaClient.objects.get_or_create(
            Channel=channel,
            ChannelUserId=channel_user_id,
            defaults={'ConversationId': Conversation.objects.create()}
        )

        conversation = rasa_client.ConversationId

        # ===================================
        # 3. RÉCUPÉRER / CRÉER ACTOR CLIENT
        # ===================================
        client_actor, _ = Actor.objects.get_or_create(
            rasa_client=rasa_client,
            defaults={
                'actor_type': 'client',
            
            }
        )

        # ===================================
        # 4. SAUVEGARDER MESSAGE UTILISATEUR
        # ===================================
        user_message = Message.objects.create(
            conversation=conversation,
            sender=client_actor,
            content=message_text,
            reply_to=None
        )
        # =========================
        # 5. APPEL RASA API
        # =========================
        try:
            rasa_response = requests.post(
                "http://chatbot:5005/webhooks/rest/webhook",
                json={
                    "sender": channel_user_id,
                    "message": message_text
                }
            )
            rasa_data = rasa_response.json()
        except Exception:
            return Response(
                {'error': 'Rasa server unreachable'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # =========================
        # 6. CRÉER ACTOR BOT
        # =========================
        bot_actor, _ = Actor.objects.get_or_create(
            actor_type='bot',
            name='TELI Bot'
        )

    # =========================
    # 7. SAUVEGARDER RÉPONSES BOT
    # =========================
        bot_messages = []

        for r in rasa_data:
            text = r.get('text', '')

            msg = Message.objects.create(
                conversation=conversation,
                sender=bot_actor,
                content=text,
                reply_to=user_message
            )
        bot_messages.append(text)

        if msg.message_type == 'escalation':
            Notification.objects.create(
                Message=msg,
                gravity='escalation',
                context=conversation.get_conversation_context(conversation)
            )
        elif msg.message_type == 'system':
            Notification.objects.create(
                Message=msg,
                gravity='system',
                context=conversation.get_conversation_context(conversation)
            )

    # =========================
    # 8. RÉPONSE API          #
    # =========================
        return Response({
            "conversation_id": conversation.id,
            "context": conversation.get_conversation_context(conversation),
            "user_message": message_text,
            "bot_responses": bot_messages
        }, status=status.HTTP_200_OK)

    