from django.contrib import admin
from django.urls import path, include  
from .views import ConversationViewSet

urlpatterns = [
    path('view-conversation/<str:ChannelUserId>/', ConversationViewSet.as_view({'get': 'view_conversation'}), name='view_conversation'),
    path('view-single-message/<int:message_id>/', ConversationViewSet.as_view({'get': 'view_single_message'}), name='view_single_message'),
    path('list-conversations/', ConversationViewSet.as_view({'get': 'list_conversations'}), name='list_conversations'),
    path('list-messages/', ConversationViewSet.as_view({'get': 'list_messages'}), name='list_messages'),
    path('modify-message/<int:message_id>/', ConversationViewSet.as_view({'patch': 'modify_message'}), name='modify_message'),
    path('close-conversation/<int:conversation_id>/', ConversationViewSet.as_view({'post': 'close_conversation'}), name='close_conversation'),
    path('delete-conversation/<int:conversation_id>/', ConversationViewSet.as_view({'delete': 'delete_conversation'}), name='delete_conversation'),
]   