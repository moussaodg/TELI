from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WebhookViewSet

router = SimpleRouter()
router.register(r'', WebhookViewSet, basename='webhook')

urlpatterns = [
    path('', include(router.urls)),
]
