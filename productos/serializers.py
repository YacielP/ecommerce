from rest_framework import serializers
from .models import Tienda, Producto, Inventario

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'

    def validate_propietario(self, value):
        if value.rol != 'tienda':
            raise serializers.ValidationError('Solo los usuarios con el rol de "tienda" pueden ser propietarios de una tienda.')
        return value
    
class Producto(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate(self, data):
        if data['cantidad'] < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return data
