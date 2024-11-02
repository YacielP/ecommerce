from rest_framework import serializers
from .models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.SerializerMethodField()
    nombre_tienda = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'nombre_tienda', 'nombre_usuario', 'texto', 'fecha_creacion']

    def get_nombre_tienda(self, obj):
        return obj.inventario_producto.inventario.tienda.nombre
    
    def get_nombre_usuario(self, obj):
        return obj.usuario.username
