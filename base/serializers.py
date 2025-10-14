from rest_framework import serializers
from django.contrib.auth.models import User

#InventoryItemSerializer
from rest_framework import serializers
from .models import InventoryItem


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['user', 'date_added', 'last_updated']
