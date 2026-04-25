from rest_framework import serializers
from .models import role, Administrator

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = role
        fields = ['authorisation']  


class AdministratorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'tel', 'address', 'role']

    def create(self, validated_data):
        # Ensure password is hashed so Django authentication works.
        return Administrator.objects.create_user(**validated_data)

class UptadeAdministratorTelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ['tel']

class UpgradeAdministratorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ['role']




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
