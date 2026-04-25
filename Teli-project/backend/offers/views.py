from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DailyOffer, SpecialOffer, Offer
from .serializers import DailyOfferSerializer, SpecialOfferSerializer, OfferSerializer, UpdateOfferSerializer
from django.utils import timezone 
from rasaclient.serializers import RasaClientSerializer 
from rasaclient.models import RasaClient  

class OfferConfigurationsViewSet(viewsets.ViewSet):

    def list(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def ConfigureOffer(self, request):
        user = request.user
        print(f"DEBUG: user={user}, is_authenticated={user.is_authenticated}")
        print(f"DEBUG: Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        
        if not user.is_authenticated:
            return Response({'message': f'User not authenticated - user: {user}, auth header: {request.META.get("HTTP_AUTHORIZATION")}'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(configurator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def update_offer(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateOfferSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def list_offers(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_daily_offers(self, request):
        daily_offers = DailyOffer.objects.all()
        serializer = DailyOfferSerializer(daily_offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_active_offers(self, request):
        today = timezone.now().date()
        offers = Offer.objects.filter(daily_offer__day=today) | Offer.objects.filter(
            special_offer__start_date__lte=today,
            special_offer__end_date__gte=today,
        )
        offers = offers.distinct()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_special_offers(self, request):
        special_offers = SpecialOffer.objects.all()
        serializer = SpecialOfferSerializer(special_offers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            offer = Offer.objects.get(pk=pk)
            offer.delete()
            return Response({'message': 'Offre supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

class RasaCLientManagementViewSet(viewsets.ViewSet):
    def list_all_rasa_clients(self, request):
        if (
            not request.user.is_authenticated
            or not request.user.role
            or request.user.role.authorisation != 'superadmin'
        ):
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        rasa_clients = RasaClient.objects.all()
        serializer = RasaClientSerializer(rasa_clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_single_rasa_client(self, request, pk=None):
        if (
            not request.user.is_authenticated
            or not request.user.role
            or request.user.role.authorisation != 'superadmin'
        ):
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            rasa_client = RasaClient.objects.get(pk=pk)
            serializer = RasaClientSerializer(rasa_client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RasaClient.DoesNotExist:
            return Response({'message': 'RasaClient not found'}, status=status.HTTP_404_NOT_FOUND)
            

        
