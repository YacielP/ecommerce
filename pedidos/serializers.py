from rest_framework import serializers
from .models import ItemCarrito

class ItemCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrito
        fields = ['producto', 'cantidad']
