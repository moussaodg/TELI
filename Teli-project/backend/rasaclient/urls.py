from django.urls import path, include
from .views import RasaClientViewSet


urlpatterns = [
    path('send_message/', RasaClientViewSet.as_view({'post': 'send_message'}), name='send_message'),
]