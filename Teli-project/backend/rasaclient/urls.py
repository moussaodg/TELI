from django.urls import path
from .views import RasaClientViewSet, RasaClientManagementViewSet


urlpatterns = [
    path('send_message/', RasaClientViewSet.as_view({'post': 'send_message'}), name='send_message'),
    path('list/', RasaClientManagementViewSet.as_view({'get': 'list_all_rasa_clients'}), name='list_rasa_clients'),
    path('<int:pk>/', RasaClientManagementViewSet.as_view({'get': 'list_single_rasa_client'}), name='single_rasa_client'),
]