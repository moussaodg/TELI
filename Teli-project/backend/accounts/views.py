#from multiprocessing.managers import Token
from rest_framework.authtoken.models import Token
import token
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import role, Administrator
from .serializers import RoleSerializer, AdministratorSerializer, LoginSerializer, UptadeAdministratorTelSerializer, UpgradeAdministratorRoleSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.shortcuts import redirect as red
from rest_framework import status

class AdministratorManagementViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

    @action(detail=True, methods=['get'])
    def seeInfo(self, request, pk=None):
        administrator = self.get_object()
        serializer = self.get_serializer(administrator)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def Register(self, request):
        serializer = AdministratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Creation de compte reussie', 'data': serializer.data}, status = 201)        

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user) # Garde la session active pour le panel admin
            token, created = Token.objects.get_or_create(user=user)
            return Response({''
            'message': 'Connexion reussie',
            'token': token.key,  
            'user_id': user.pk
            }, status=200)
        else:
            return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request):
        logout(request)
        return Response({'message': 'Deconnexion reussie'})    

    @action(detail=True, methods=['patch'])
    def update_tel(self, request, pk=None):
        administrator = self.get_object()
        serializer = UptadeAdministratorTelSerializer(administrator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        administrator = self.get_object()
        serializer = UpgradeAdministratorRoleSerializer(administrator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

