from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import NotificationManagementViewset

router = SimpleRouter()
router.register(r'', NotificationManagementViewset, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]