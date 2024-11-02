from rest_framework import viewsets
from .models import Comentario
from productos.models import InventarioProducto
from .serializers import ComentarioSerializer
from productos.permissions import EsCompradorOPropietario
from .permissions import IsOwnerComentario


"""
AQUI HAY Q ARREGLAR LA TALLA DE LOS PERMISOS
"""
class ComentarioViewSet(viewsets.ModelViewSet):
    serializer_class = ComentarioSerializer
    permission_classes = [EsCompradorOPropietario]

    def get_queryset(self):
        tienda_id = self.kwargs['tienda_id']
        inventario_producto_id = self.kwargs['inventario_producto_id']
        return Comentario.objects.filter(
            inventario_producto__inventario__tienda_id=tienda_id,
            inventario_producto_id=inventario_producto_id
        )
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerComentario]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [EsCompradorOPropietario]
        return super().get_permissions()

    def perform_create(self, serializer):
        producto = InventarioProducto.objects.get(id=self.kwargs['inventario_producto_id'])
        serializer.save(usuario=self.request.user, inventario_producto=producto)
