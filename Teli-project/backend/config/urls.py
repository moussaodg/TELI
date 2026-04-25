from django.contrib import admin
from django.urls import path, include

urlpatterns = [
       path('administrators/', include('accounts.urls')),
       path('offers/', include('offers.urls')),
       path('conversations/', include('conversations.urls')),
       path('rasaclient/', include('rasaclient.urls')),
       path('notifications/', include('notifications.urls')),
       path('webhook/', include('webhook.urls')),
       path('statistics/', include('stats.urls')),
       
]
