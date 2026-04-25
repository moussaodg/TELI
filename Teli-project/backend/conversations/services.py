from django.core.exceptions import ObjectDoesNotExist
from .models import Conversation, Message


class ConversationService:
    @staticmethod
    def get_conversation_by_channel_user(channel_user_id):
        return Conversation.objects.get(rasa_clients__ChannelUserId=channel_user_id)

    @staticmethod
    def list_conversations():
        return Conversation.objects.all()

    @staticmethod
    def list_messages():
        return Message.objects.all()

    @staticmethod
    def get_message(message_id):
        return Message.objects.get(id=message_id)

    @staticmethod
    def update_message(message, data):
        for attr, value in data.items():
            setattr(message, attr, value)
        message.save()
        return message

    @staticmethod
    def close_conversation(conversation):
        conversation.is_satisfied = True
        conversation.status = 'CLOSED'
        conversation.save()
        return conversation

    @staticmethod
    def reopen_conversation(conversation):
        conversation.is_satisfied = False
        conversation.status = 'BOT_ACTIVE'
        conversation.save()
        return conversation

    @staticmethod
    def assign_conversation(conversation, administrator):
        if conversation.administrator is not None:
            raise ValueError('Conversation already taken in charge')
        conversation.administrator = administrator
        conversation.status = 'HUMAN_ACTIVE'
        conversation.save()
        return conversation

    @staticmethod
    def delete_message(message):
        message.delete()
