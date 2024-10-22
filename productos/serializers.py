from rest_framework import serializers
from .models import Tienda, Producto, Inventario

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

    
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_nombre(self, data):
        if len(data) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return data

    def validate(self, data):
        if data['cantidad'] < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return data
