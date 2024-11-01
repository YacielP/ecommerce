from rest_framework import serializers
from .models import Comentario
from usuarios.models import Usuario
from productos.models import InventarioProducto

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username']
        
class TiendaDelProducto(serializers.ModelSerializer):
    tienda_nombre = serializers.SerializerMethodField()

    class Meta:
        model = InventarioProducto
        fields = ['tienda_nombre']

    def get_tienda_nombre(self, obj):
        return obj.inventario.tienda.nombre


class ComentarioSerializer(serializers.ModelSerializer):
    usuario = UsernameSerializer(read_only=True)
    inventario_producto = TiendaDelProducto(read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'inventario_producto', 'usuario', 'texto', 'fecha_creacion']
