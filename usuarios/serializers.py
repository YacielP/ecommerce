from rest_framework import serializers
from .models import Usuario, UsuarioComprador, UsuarioPropietario

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'direccion', 'telefono', 'rol']

    def create(self, validated_data):
        if Usuario.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya existe"})
        if Usuario.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Este correo electrónico ya existe"})

        user = Usuario.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # Este método cifrará la contraseña automáticamente
            direccion=validated_data.get('direccion', ''),
            telefono=validated_data.get('telefono', ''),
            rol=validated_data.get('rol', 'comprador')
        )
        return user

class CompradorSerializer(RegistroSerializer):

    class Meta:
        model = UsuarioComprador
        fields = RegistroSerializer.Meta.fields + ['puntos']

class PropietarioSerializer(RegistroSerializer):

    class Meta:
        model = UsuarioPropietario
        fields = RegistroSerializer.Meta.fields

class UpdateCompradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioComprador
        fields = ['first_name', 'last_name', 'direccion', 'telefono']

class UpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ['rol']