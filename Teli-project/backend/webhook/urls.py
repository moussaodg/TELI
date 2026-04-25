from django.urls import path
from .views import WebhookViewSet

urlpatterns = [
    path('verify/', WebhookViewSet.as_view({'get': 'verify'}), name='verify_webhook'),
    path('receive/', WebhookViewSet.as_view({'post': 'receive'}), name='receive_webhook'),
]
