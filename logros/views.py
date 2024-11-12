from rest_framework import viewsets
from .models import Logro
from .serializers import LogroSerializer, LogroTiendaSerializer, LogroUsuarioSerializer

class LogroViewSet(viewsets.ModelViewSet):
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer