from rest_framework import serializers
from .models import Tienda, ProductoCentral, InventarioProducto
from categorias.serializers import CategoriaSerializer

class ProductoCentralSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ProductoCentral
        fields = ['id', 'nombre', 'descripcion', 'categoria_nombre']

    def get_categoria_nombre(self, obj):
        return obj.categoria.nombre

class InventarioProductoSerializer(serializers.ModelSerializer):
    tienda_nombre = serializers.SerializerMethodField()
    producto_central_nombre = serializers.SerializerMethodField()
    categoria_nombre = serializers.SerializerMethodField()

    class Meta:
        model = InventarioProducto
        fields = ['id', 'cantidad', 'precio_personalizado', 'resenna', 'tienda_nombre',
                   'producto_central_nombre', 'categoria_nombre']

    def get_tienda_nombre(self, obj):
        return obj.inventario.tienda.nombre
    
    def get_producto_central_nombre(self, obj):
        return obj.producto_central.nombre
    
    def get_categoria_nombre(self, obj):
        return obj.producto_central.categoria.nombre


class TiendaSerializer(serializers.ModelSerializer):
    nombre_propietario = serializers.SerializerMethodField()

    class Meta:
        model = Tienda
        fields = ['id', 'nombre', 'direccion', 'descripcion', 'nombre_propietario']
        extra_kwargs = {
            'propietario': {'read_only': True}
        }
    
    def get_nombre_propietario(self, obj):
        return obj.propietario.first_name

    def validate_propietario(self, data):
        if data.rol != 'propietario':
            raise serializers.ValidationError('Solo los usuarios con el rol de "propietario" pueden ser propietarios de una tienda.')
        return data
    
    def validate_nombre(self, data):
        if len(data) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return data

    def validate_direccion(self, data):
        if len(data) < 5:
            raise serializers.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return data
