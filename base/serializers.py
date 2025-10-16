from rest_framework import serializers
from django.contrib.auth.models import User

#InventoryItemSerializer
from .models import InventoryItem, InventoryChange


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

class InventoryChangeSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = InventoryChange
        fields = ['id', 'item_name', 'old_quantity', 'new_qunatity', 'change_date']
