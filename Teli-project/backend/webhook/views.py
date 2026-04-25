from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from rasaclient.services import RasaClientService


class WebhookViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def verify(self, request):
        mode = request.query_params.get('hub.mode')
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        expected = getattr(settings, 'WEBHOOK_VERIFY_TOKEN', 'TELI_VERIFY_TOKEN')
        if mode == 'subscribe' and token == expected:
            return Response(challenge, status=status.HTTP_200_OK)
        return Response({'error': 'Verification failed'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def receive(self, request):
        entries = request.data.get('entry', [])
        results = []

        for entry in entries:
            for messaging_event in entry.get('messaging', []):
                sender = messaging_event.get('sender', {}).get('id')
                message_text = messaging_event.get('message', {}).get('text')
                if sender and message_text:
                    conversation, user_message, bot_messages = RasaClientService.process_incoming_message(
                        channel='facebook',
                        channel_user_id=sender,
                        message_text=message_text,
                    )
                    results.append({
                        'conversation_id': conversation.id,
                        'bot_responses': [msg.content for msg in bot_messages],
                    })

        return Response({'results': results}, status=status.HTTP_200_OK)
