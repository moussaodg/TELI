from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import OfferConfigurationsViewSet

router = SimpleRouter()
router.register(r'', OfferConfigurationsViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),
]