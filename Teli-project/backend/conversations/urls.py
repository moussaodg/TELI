from django.urls import path
from .views import ConversationViewSet, ConversationManagementViewset

urlpatterns = [
    path('view-conversation/<str:channel_user_id>/', ConversationViewSet.as_view({'get': 'view_conversation'}), name='view_conversation'),
    path('view-single-message/<int:message_id>/', ConversationViewSet.as_view({'get': 'view_single_message'}), name='view_single_message'),
    path('list-conversations/', ConversationViewSet.as_view({'get': 'list_conversations'}), name='list_conversations'),
    path('list-messages/', ConversationViewSet.as_view({'get': 'list_messages'}), name='list_messages'),
    path('modify-message/<int:message_id>/', ConversationViewSet.as_view({'patch': 'modify_message'}), name='modify_message'),
    path('close-conversation/<int:conversation_id>/', ConversationViewSet.as_view({'post': 'close_conversation'}), name='close_conversation'),
    path('reopen-conversation/<str:channel_user_id>/', ConversationViewSet.as_view({'post': 'reopen_conversation'}), name='reopen_conversation'),
    path('delete-message/<int:message_id>/', ConversationViewSet.as_view({'delete': 'delete_message'}), name='delete_message'),
    path('assign-conversation/<int:conversation_id>/', ConversationManagementViewset.as_view({'post': 'prendre_en_charge_conversation'}), name='assign_conversation'),
    path('delete-conversation/<int:conversation_id>/', ConversationViewSet.as_view({'delete': 'delete_conversation'}), name='delete_conversation'),
]   