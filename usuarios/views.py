from rest_framework import generics, permissions
from .models import Usuario
from .serializers import RegistroSerializer
from .permissions import IsDuenno

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAdminUser]

class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer

    """!!!!!!!!!!HAY PROBLEMAS PARA Q UN USUARIO ELIMINE Y ACTUALICE SU PROPIA CUENTA(LO MISMO CON EL ADMIN)"""
    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos  los usuarios pueden ver los detalles del resto de usuarios
            return [permissions.IsAuthenticated()]
        elif self.request.method in ['PUT', 'DELETE']:
            #Solo los usuarios dueños de sus cuentas o administradores pueden eliminarla o actualizarla
            return [permissions.IsAdminUser(), IsDuenno()]
        return [permissions.IsAuthenticated()]  # Default a `IsAuthenticated` para otros métodos
