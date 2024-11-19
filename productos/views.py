from rest_framework import generics, permissions, viewsets
from usuarios.permissions import EsUsuarioTienda, EsUsuarioComprador
from .permissions import EsCompradorOPropietario, IsOwner
from .serializers import TiendaSerializer, ProductoCentralSerializer, InventarioProductoSerializer
from .models import Tienda, ProductoCentral, Inventario, InventarioProducto
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import InventarioProductoFilter
from rest_framework import viewsets
from categorias.models import Categoria
from rest_framework import serializers
from usuarios.models import Propietario

class InventarioProductoViewSet(viewsets.ModelViewSet):
    queryset = InventarioProducto.objects.all()
    serializer_class = InventarioProductoSerializer
    permission_classes = [EsUsuarioComprador]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventarioProductoFilter

class MostrarCatalogoView(generics.ListAPIView):
    serializer_class = InventarioProductoSerializer
    permission_classes = [EsCompradorOPropietario]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventarioProductoFilter

    def get_queryset(self):
        tienda_id = self.kwargs['tienda_id']
        try:
            tienda = Tienda.objects.get(id=tienda_id)
            inventario = Inventario.objects.get(tienda=tienda)
            return InventarioProducto.objects.filter(inventario=inventario)
        except Tienda.DoesNotExist:
            return InventarioProducto.objects.none()

class EliminarProductoInventarioView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        tienda_id = pk
        nombre_producto = request.data.get('nombre_producto')
        cantidad = int(request.data.get('cantidad'))

        inventario = Inventario.objects.get(tienda__id=tienda_id)
        producto = InventarioProducto.objects.get(inventario=inventario, producto_central__nombre=nombre_producto)

        if producto:
            if cantidad < producto.cantidad:
                producto.cantidad -= cantidad
                producto.save()
                return Response({'message': 'Producto actualizado en el inventario'}, status=status.HTTP_200_OK)
            elif cantidad == producto.cantidad:
                producto.delete()
                return Response({'message': 'Producto eliminado del inventario'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'La cantidad que desea eliminar es mayor que la cantidad real'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'error': 'Producto no encontrado en el inventario.'}, status=status.HTTP_404_NOT_FOUND)
        

class AgregarProductoInventarioView(APIView):
    def post(self, request, tienda_id, *args, **kwargs):
        nombre_producto = request.data.get('nombre_producto')
        cantidad = request.data.get('cantidad')
        precio_personalizado = request.data.get('precio_personalizado')
        descripcion = request.data.get('descripcion', '')
        descripcion_categoria = request.data.get('descripcion_categoria', '')
        nombre_categoria = request.data.get('nombre_categoria', '')

        #Verificar si la categoria ya existe
        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre_categoria,
            defaults={'descripcion': descripcion_categoria}
        )

        # Verificar si el producto ya existe
        producto, created = ProductoCentral.objects.get_or_create(
            nombre=nombre_producto, 
            defaults={'descripcion': descripcion, 'categoria': categoria}
        )

        # Obtener el inventario de la tienda
        inventario = Inventario.objects.get(tienda__id=tienda_id)

        # Verificar si ya existe en el inventario
        inventario_producto, inventario_created = InventarioProducto.objects.get_or_create(
            inventario=inventario,
            producto_central=producto,
            defaults={'cantidad': cantidad, 'precio_personalizado': precio_personalizado}
        )

        if not inventario_created:
            # Si ya existe, actualizar la cantidad y el precio personalizado
            inventario_producto.cantidad += int(cantidad)
            inventario_producto.precio_personalizado = precio_personalizado  # Actualizar el precio personalizado
            inventario_producto.save()

        return Response({
            'producto': ProductoCentralSerializer(producto).data,
            'inventario_producto': InventarioProductoSerializer(inventario_producto).data
        }, status=status.HTTP_201_CREATED)
    
class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [EsUsuarioComprador()]
        elif self.action == 'create':
            return [EsUsuarioTienda()]
        elif self.action == 'retrieve':
            return [EsUsuarioComprador()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()
    
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        #Verifica si el usuario es un propietario
        if self.request.user.rol == 'propietario':
            propietario = Propietario.objects.get(id=self.request.user.id)
            serializer.save(propietario=propietario)
        else:
            raise serializers.ValidationError("El usuario autenticado no es propetario")