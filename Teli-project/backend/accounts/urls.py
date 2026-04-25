from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AdministratorManagementViewSet

router = SimpleRouter()
router.register(r'', AdministratorManagementViewSet, basename='administrator')

urlpatterns = [
    path('', include(router.urls)),
]
