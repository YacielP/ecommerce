from rest_framework import generics, permissions
from usuarios.permissions import EsUsuarioTienda, EsUsuarioComprador, IsDuenno
from .serializers import TiendaSerializer, ProductoCentralSerializer, InventarioProductoSerializer
from .models import Tienda, ProductoCentral, Inventario, InventarioProducto
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import InventarioProductoFilter

class MostrarCatalogoView(generics.ListAPIView):
    serializer_class = InventarioProductoSerializer
    permission_classes = [IsDuenno, EsUsuarioComprador]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventarioProductoFilter

    def get_queryset(self):
        tienda_id = self.kwargs['pk']
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
    def post(self, request, pk, *args, **kwargs):
        tienda_id = pk
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


class ProductoCreateView(generics.CreateAPIView):
    queryset = ProductoCentral.objects.all()
    serializer_class = ProductoCentral
    permission_classes = [EsUsuarioTienda]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductoCentral.objects.all()
    serializer_class = ProductoCentral

    def get_permissions(self):
        if self.request.method == 'GET':
            #Solo los propietarios o un usuario comprador puede ver los detalles de un producto
            return [IsDuenno(), EsUsuarioComprador()]
        
        elif self.request.method == 'PUT':
            #Solo los propietqarios pueden actualizar un producto
            return [IsDuenno()]
        
        elif self.request.method == 'DELETE':
            #Solo los propietarios o los administradores pueden borrar un producto
            return [IsDuenno(), permissions.IsAdminUser()]
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
            return [IsDuenno()]
        elif self.request.method == 'DELETE':
            #solo los propietarios y administradores pueden eliminar una tienda
            return [IsDuenno(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
