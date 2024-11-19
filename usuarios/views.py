from rest_framework import generics, permissions
from .models import Usuario, Comprador, Propietario
from .serializers import RegistroSerializer, CompradorSerializer, PropietarioSerializer, UpdateAdminSerializer, UpdateCompradorSerializer
from .permissions import IsAdminOrPropieratio, IsOwnerOrAdminOrPropietario, IsAdminOrComprador, IsOwnerOrAdminOrComprador
from rest_framework import viewsets

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]
    
class CompradorViewSet(viewsets.ModelViewSet):
    queryset = Comprador
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
        return CompradorSerializer
    
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        serializer.save()

class PropietarioViewSet(viewsets.ModelViewSet):
    queryset = Propietario.objects.all()
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
        return PropietarioSerializer
        
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        serializer.save()