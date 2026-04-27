from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import DailyOffer, SpecialOffer
from .serializers import DailyOfferSerializer, SpecialOfferSerializer, OfferSerializer
from .services import OfferService

class OfferConfigurationsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        daily_offers = DailyOffer.objects.all()
        special_offers = SpecialOffer.objects.all()
        offers = list(daily_offers) + list(special_offers)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if not getattr(user, 'role', None) or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)

        offer_type = request.data.get('offer_type')
        if offer_type == 'daily':
            serializer = DailyOfferSerializer(data=request.data)
        elif offer_type == 'special':
            serializer = SpecialOfferSerializer(data=request.data)
        else:
            return Response({'offer_type': 'Le type d offre doit être "daily" ou "special".'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(configurator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        offer = self._get_offer_by_pk(pk)
        if offer is None:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSerializer(offer)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'Unauthorized - superadmin required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        offer = self._get_offer_by_pk(pk)
        if offer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DailyOfferSerializer(offer, data=request.data, partial=True) if isinstance(offer, DailyOffer) else SpecialOfferSerializer(offer, data=request.data, partial=True)
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
        
        offer = self._get_offer_by_pk(pk)
        if offer is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        offer.delete()
        return Response({'message': 'Offre supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
    
    def list_daily_offers(self, request):
        daily_offers = OfferService.list_daily_offers()
        serializer = DailyOfferSerializer(daily_offers, many=True)
        return Response(serializer.data)

    def _get_offer_by_pk(self, pk):
        try:
            return DailyOffer.objects.get(pk=pk)
        except DailyOffer.DoesNotExist:
            try:
                return SpecialOffer.objects.get(pk=pk)
            except SpecialOffer.DoesNotExist:
                return None
    
