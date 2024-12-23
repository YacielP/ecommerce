from rest_framework import serializers
from .models import Tienda, ProductoCentral, InventarioProducto
from categorias.serializers import CategoriaSerializer

class ProductoCentralSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()

    class Meta:
        model = ProductoCentral
        fields = ['id', 'nombre', 'descripcion', 'categoria']

class InventarioProductoSerializer(serializers.ModelSerializer):
    tienda_nombre = serializers.SerializerMethodField()
    producto_central = ProductoCentralSerializer()

    class Meta:
        model = InventarioProducto
        fields = ['id', 'producto_central', 'cantidad', 'precio_personalizado', 'resenna', 'tienda_nombre']

    def get_tienda_nombre(self, obj):
        return obj.inventario.tienda.nombre


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
