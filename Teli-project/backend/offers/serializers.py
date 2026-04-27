from .models import DailyOffer, SpecialOffer
from rest_framework import serializers


class DailyOfferSerializer(serializers.ModelSerializer):
    offer_type = serializers.SerializerMethodField()

    class Meta:
        model = DailyOffer
        fields = '__all__'
        read_only_fields = ['configurator']

    def get_offer_type(self, obj):
        return 'daily'


class SpecialOfferSerializer(serializers.ModelSerializer):
    offer_type = serializers.SerializerMethodField()

    class Meta:
        model = SpecialOffer
        fields = '__all__'
        read_only_fields = ['configurator']

    def get_offer_type(self, obj):
        return 'special'


class OfferSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, DailyOffer):
            return DailyOfferSerializer(instance).data
        if isinstance(instance, SpecialOffer):
            return SpecialOfferSerializer(instance).data
        return super().to_representation(instance)

