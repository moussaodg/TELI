from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RasaClientViewSet, RasaClientManagementViewSet

router = SimpleRouter()
router.register(r'', RasaClientViewSet, basename='rasa-client-message')
router.register(r'clients', RasaClientManagementViewSet, basename='rasa-client')

urlpatterns = [
    path('', include(router.urls)),
]