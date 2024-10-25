from rest_framework import generics, permissions
from usuarios.permissions import EsUsuarioTienda, EsUsuarioComprador
from .permissions import IsPropietario
from .serializers import TiendaSerializer, ProductoSerializer
from .models import Tienda, ProductoCentral, Inventario, InventarioProducto
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductoCentralSerializer, InventarioProductoSerializer

class AgregarProductoInventarioView(APIView):
    def post(self, request, *args, **kwargs):
        tienda_id = request.data.get('tienda_id')
        nombre_producto = request.data.get('nombre_producto')
        cantidad = request.data.get('cantidad')
        precio_personalizado = request.data.get('precio_personalizado')
        descripcion = request.data.get('descripcion', '')

        # Verificar si el producto ya existe
        producto, created = ProductoCentral.objects.get_or_create(
            nombre=nombre_producto, 
            defaults={'descripcion': descripcion}
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


class ProductoListView(generics.ListAPIView):
    queryset = ProductoCentral.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductoCreateView(generics.CreateAPIView):
    queryset = ProductoCentral.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [EsUsuarioTienda]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductoCentral.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            #Solo los propietarios o un usuario comprador puede ver los detalles de un producto
            return [IsPropietario(), EsUsuarioComprador()]
        
        elif self.request.method == 'PUT':
            #Solo los propietqarios pueden actualizar un producto
            return [IsPropietario()]
        
        elif self.request.method == 'DELETE':
            #Solo los propietarios o los administradores pueden borrar un producto
            return [IsPropietario(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
class TiendaListView(generics.ListAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [permissions.IsAuthenticated]

class TiendaCreateView(generics.CreateAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [EsUsuarioTienda]

class TiendaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            #Solo los usuarios compradores y los administradores pueden ver detalles de tiendas
            return [EsUsuarioComprador(), permissions.IsAdminUser()]
        elif self.request.method == 'PUT':
            #solo los propietarios pueden actualizar su tienda
            return [IsPropietario()]
        elif self.request.method == 'DELETE':
            #solo los propietarios y administradores pueden eliminar una tienda
            return [IsPropietario(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
