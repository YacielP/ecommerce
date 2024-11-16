from rest_framework import generics, permissions
from .models import Usuario, UsuarioComprador, UsuarioPropietario
from .serializers import RegistroSerializer, CompradorSerializer, PropietarioSerializer, UpdateAdminSerializer, UpdateCompradorSerializer
from .permissions import IsAdminOrPropieratio, IsOwnerOrAdminOrPropietario, IsAdminOrComprador, IsOwnerOrAdminOrComprador
from rest_framework import viewsets

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]
    
class UsuarioCompradorViewSet(viewsets.ModelViewSet):
    queryset = UsuarioComprador
    serializer_class = CompradorSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminOrPropieratio()]
        elif self.action == 'retrieve':
            return [IsOwnerOrAdminOrPropietario()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminOrPropietario()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            #Verificar si el usuario es administrador
            if self.request.user.is_staff:
                return UpdateAdminSerializer
            return UpdateCompradorSerializer
        return UpdateCompradorSerializer
    
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

class UsuarioPropietarioViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPropietario.objects.all()
    serializer_class = PropietarioSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminOrComprador()]
        elif self.action == 'retrieve':
            return [IsOwnerOrAdminOrComprador()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminOrComprador()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateAdminSerializer
        
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj