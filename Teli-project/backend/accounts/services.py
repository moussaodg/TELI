from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token

from .models import Administrator


class AdministratorService:
    @staticmethod
    def create_administrator(data):
        administrator = Administrator.objects.create(**data)
        return administrator

    @staticmethod
    def authenticate_user(request, username, password):
        return authenticate(request, username=username, password=password)

    @staticmethod
    def create_token_for_user(user):
        token, _ = Token.objects.get_or_create(user=user)
        return token

    @staticmethod
    def login_user(request, user):
        django_login(request, user)

    @staticmethod
    def logout_user(request):
        django_logout(request)
