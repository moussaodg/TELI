from django.contrib import admin
from django.urls import path, include  
from . import views 

urlpatterns = [
    path('', views.AdministratorManagementViewSet.as_view({'get': 'list', 'post': 'Register'}), name='administrator-list'),
    path('<int:pk>/see-info/', views.AdministratorManagementViewSet.as_view({'get': 'seeInfo'}), name='administrator-see-info'),
    path('<int:pk>/update_tel/', views.AdministratorManagementViewSet.as_view({'patch': 'update_tel'}), name='administrator-update-tel'),
    path('<int:pk>/update_role/', views.AdministratorManagementViewSet.as_view({'patch': 'update_role'}), name='administrator-update-role'),
    path('login/', views.AdministratorManagementViewSet.as_view({'post': 'login'}), name='administrator-login'),
    path('logout/', views.AdministratorManagementViewSet.as_view({'post': 'logout'}), name='administrator-logout'),
]
