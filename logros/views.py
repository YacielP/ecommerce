from rest_framework import viewsets, permissions
from .models import Logro
from .serializers import LogroSerializer, LogroTiendaSerializer, LogroUsuarioSerializer

class LogroViewSet(viewsets.ModelViewSet):
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer
    permission_classes = [permissions.IsAdminUser]