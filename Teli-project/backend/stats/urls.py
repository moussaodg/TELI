from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DashboardStatisticsViewSet

router = SimpleRouter()
router.register(r'', DashboardStatisticsViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
