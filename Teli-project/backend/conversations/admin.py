from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_satisfied', 'start_date', 'last_activity')
    search_fields = ('context',)
    list_filter = ('status', 'is_satisfied', 'start_date')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'message_type', 'status', 'timestamp')
    search_fields = ('content',)
    list_filter = ('message_type', 'status', 'timestamp')
