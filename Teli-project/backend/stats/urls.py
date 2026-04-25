from django.urls import path
from .views import DashboardStatisticsViewSet

urlpatterns = [
    path('dashboard/', DashboardStatisticsViewSet.as_view({'get': 'dashboard'}), name='dashboard_statistics'),
]
