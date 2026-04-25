from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('configure-offer/', views.OfferConfigurationsViewSet.as_view({"post": "ConfigureOffer"}), name = "Offer-Configuration"),
    path('<int:pk>/update-offer/', views.OfferConfigurationsViewSet.as_view({"patch": "update_offer"}), name = "Offer-update"),
    path('list-offers/', views.OfferConfigurationsViewSet.as_view({"get": "list_offers"}), name = "list_all_offers"),
    path('list-active-offers/', views.OfferConfigurationsViewSet.as_view({"get": "list_active_offers"}), name = "list_active_offers"),
    path('list-daily-offers/', views.OfferConfigurationsViewSet.as_view({"get": "list_daily_offers"}), name = "list_daily_offers"),
    path('list-special-offers/', views.OfferConfigurationsViewSet.as_view({"get": "list_special_offers"}), name = "list_special_offers"),
    path('<int:pk>/delete/', views.OfferConfigurationsViewSet.as_view({"delete": "delete"}), name = "delete_offer"),
    path('list-rasa-clients/', views.OfferConfigurationsViewSet.as_view({"get": "list_all_rasa_clients"}), name = "list_all_rasa_clients"),
    path('rasa-client/<int:pk>/', views.OfferConfigurationsViewSet.as_view({"get": "list_single_rasa_client"}), name = "list_single_rasa_client"),
]