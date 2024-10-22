from rest_framework import generics, permissions
from usuarios.permissions import EsUsuarioTienda, EsUsuarioComprador
from .permissions import IsPropietario
from .serializers import TiendaSerializer, ProductoSerializer
from .models import Tienda, Producto

class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [EsUsuarioTienda]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
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