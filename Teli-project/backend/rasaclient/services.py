import requests
from .models import RasaClient
from conversations.models import Conversation, Actor, Message
from notifications.models import Notification


class RasaClientService:
    @staticmethod
    def get_or_create_client(channel, channel_user_id):
        conversation = Conversation.objects.create()
        rasa_client, _ = RasaClient.objects.get_or_create(
            Channel=channel,
            ChannelUserId=channel_user_id,
            defaults={'ConversationId': conversation}
        )
        return rasa_client

    @staticmethod
    def send_to_rasa(channel_user_id, message_text):
        response = requests.post(
            "http://chatbot:5005/webhooks/rest/webhook",
            json={"sender": channel_user_id, "message": message_text},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_or_create_client_actor(rasa_client):
        actor, _ = Actor.objects.get_or_create(
            rasa_client=rasa_client,
            defaults={
                'actor_type': 'client',
            }
        )
        return actor

    @staticmethod
    def get_or_create_bot_actor():
        bot_actor, _ = Actor.objects.get_or_create(
            actor_type='bot',
            defaults={
                'name': 'TELI Bot',
                'rasa_client': None,
                'administrator': None,
            }
        )
        return bot_actor

    @staticmethod
    def create_user_message(conversation, sender, message_text):
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=message_text,
            reply_to=None,
        )

    @staticmethod
    def create_bot_messages(conversation, bot_actor, user_message, rasa_data):
        bot_messages = []
        for item in rasa_data:
            text = item.get('text', '')
            message_type = item.get('message_type', 'text')
            msg = Message.objects.create(
                conversation=conversation,
                sender=bot_actor,
                content=text,
                message_type=message_type,
                reply_to=user_message,
            )
            bot_messages.append(msg)
        return bot_messages

    @staticmethod
    def create_notifications_for_messages(messages):
        for msg in messages:
            if msg.message_type in ('escalation', 'system'):
                Notification.objects.create(
                    conversation=msg.conversation,
                    message=msg,
                    gravity=msg.message_type,
                    context={
                        'conversation_id': msg.conversation.id,
                        'bot_response': msg.content,
                    },
                )

    @staticmethod
    def process_incoming_message(channel, channel_user_id, message_text):
        rasa_client = RasaClientService.get_or_create_client(channel, channel_user_id)
        conversation = rasa_client.ConversationId
        client_actor = RasaClientService.get_or_create_client_actor(rasa_client)
        user_message = RasaClientService.create_user_message(conversation, client_actor, message_text)
        rasa_data = RasaClientService.send_to_rasa(channel_user_id, message_text)
        bot_actor = RasaClientService.get_or_create_bot_actor()
        bot_messages = RasaClientService.create_bot_messages(conversation, bot_actor, user_message, rasa_data)
        RasaClientService.create_notifications_for_messages(bot_messages)
        return conversation, user_message, bot_messages
