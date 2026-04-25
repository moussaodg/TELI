from django.urls import path
from .views import NotificationManagementViewset, NotificationProblemeTypeListViewset

urlpatterns = [
    path('list-notifications/', NotificationManagementViewset.as_view({'get': 'list_notifications'}), name='list_notifications'),
    path('view-notification/<int:notification_id>/', NotificationManagementViewset.as_view({'get': 'view_notification'}), name='view_notification'),
    path('mark-as-read/<int:notification_id>/', NotificationManagementViewset.as_view({'post': 'mark_as_read'}), name='mark_as_read'),
    path('list-escalation-notifications/', NotificationManagementViewset.as_view({'get': 'list_escalation_notifications'}), name='list_escalation_notifications'),
    path('list-system-notifications/', NotificationManagementViewset.as_view({'get': 'list_system_notifications'}), name='list_system_notifications'),
    path('list-probleme-types/<str:problem_type>/', NotificationProblemeTypeListViewset.as_view({'get': 'list_probleme_by_type'}), name='list_probleme_by_type'),
]