from rest_framework import generics
from .models import Actividad
from .serializers import ActividadSerializer

class ListActividad(generics.ListAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer