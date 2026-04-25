from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from .models import Administrator
from .serializers import AdministratorSerializer, LoginSerializer, UptadeAdministratorTelSerializer, UpgradeAdministratorRoleSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .services import AdministratorService

class AdministratorManagementViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def see_info(self, request, pk=None):
        administrator = self.get_object()
        serializer = self.get_serializer(administrator)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = AdministratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Creation de compte reussie', 'data': serializer.data}, status = 201)        

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = AdministratorService.authenticate_user(request, username, password)
        if user is not None:
            AdministratorService.login_user(request, user)
            token = AdministratorService.create_token_for_user(user)
            return Response({
                'message': 'Connexion reussie',
                'token': token.key,
                'user_id': user.pk,
            }, status=200)
        else:
            return Response({'message': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        AdministratorService.logout_user(request)
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

