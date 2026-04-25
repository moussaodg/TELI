from .models import DailyOffer, SpecialOffer, Offer, BaseOffer
from rest_framework import serializers

class DailyOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyOffer
        fields = '__all__'

class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['code', 'price', 'special_offer', 'daily_offer']

