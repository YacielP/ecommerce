from rest_framework import serializers
from .models import Logro, LogroTienda, LogroUsuario

class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = '__all__'

class LogroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogroUsuario
        fields = '__all__'

class LogroTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogroTienda
        fields = '__all__'