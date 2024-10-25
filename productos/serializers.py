from rest_framework import serializers
from .models import Tienda, ProductoCentral, InventarioProducto

class ProductoCentralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCentral
        fields = ['id', 'nombre', 'descripcion']

class InventarioProductoSerializer(serializers.ModelSerializer):
    producto_central = ProductoCentralSerializer()

    class Meta:
        model = InventarioProducto
        fields = ['id', 'producto_central', 'cantidad', 'precio_personalizado']


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'

    def validate_propietario(self, data):
        if data.rol != 'tienda':
            raise serializers.ValidationError('Solo los usuarios con el rol de "tienda" pueden ser propietarios de una tienda.')
        return data
    
    def validate_nombre(self, data):
        if len(data) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return data

    def validate_direccion(self, data):
        if len(data) < 5:
            raise serializers.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return data
