from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import DailyOffer, SpecialOffer, Offer
from .serializers import DailyOfferSerializer, SpecialOfferSerializer, OfferSerializer, UpdateOfferSerializer
from .services import OfferService
from django.utils import timezone

class OfferConfigurationsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if not getattr(user, 'role', None) or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(configurator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSerializer(offer)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
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
    def daily(self, request):
        daily_offers = OfferService.list_daily_offers()
        serializer = DailyOfferSerializer(daily_offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        offers = OfferService.list_active_offers()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def special(self, request):
        special_offers = OfferService.list_special_offers()
        serializer = SpecialOfferSerializer(special_offers, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
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
        daily_offers = OfferService.list_daily_offers()
        serializer = DailyOfferSerializer(daily_offers, many=True)
        return Response(serializer.data)
    
    def list_daily_offers(self, request):
        daily_offers = OfferService.list_daily_offers()
        serializer = DailyOfferSerializer(daily_offers, many=True)
        return Response(serializer.data)
        
        if not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            offer = Offer.objects.get(pk=pk)
            offer.delete()
            return Response({'message': 'Offre supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
