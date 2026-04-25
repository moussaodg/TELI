from rest_framework import serializers
from .models import RasaClient

class RasaClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasaClient
        fields = '__all__'
        