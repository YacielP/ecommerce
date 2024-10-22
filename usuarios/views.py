from rest_framework import generics, permissions
from .models import Usuario
from .serializers import RegistroSerializer
from .permissions import EsUsuarioComprador, EsUsuarioTienda, IsDuenno

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

    def get_permissions(self):
        if self.request.method == 'GET':
            #Todos  los usuarios pueden ver los detalles del resto de usuarios
            return [permissions.IsAuthenticated()]
        elif self.request.method in ['PUT', 'DELETE']:
            #Solo los usuarios dueños de sus cuentas pueden eliminarla o actualizarla
            return [permissions.IsAdminUser(), IsDuenno()]
        elif self.request.method in ['PUT', 'DELETE']:
            # Solo los usuarios dueños de sus cuentas pueden eliminarlas o actualizarlas
            return [IsDuenno()]
        return [permissions.IsAuthenticated()]  # Default a `IsAuthenticated` para otros métodos
