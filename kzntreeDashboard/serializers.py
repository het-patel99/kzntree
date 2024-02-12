# myapp/serializers.py
from rest_framework import serializers
from .models import InventoryItem, BuildDashboard

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class BuildDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildDashboard
        fields = '__all__'
