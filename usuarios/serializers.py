from rest_framework import serializers
from .models import Usuario, Comprador, Propietario

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
        model = Comprador
        fields = RegistroSerializer.Meta.fields + ['puntos']

    def validate(self, data):
        if data.get('rol') != 'comprador':
            raise serializers.ValidationError("El rol debe de ser 'comprador' para crear un Comprador")
        return data

    def create(self, validated_data):
        if Usuario.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya existe"})
        if Usuario.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Este correo electrónico ya existe"})

        user = Comprador.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # Este método cifrará la contraseña automáticamente
            direccion=validated_data.get('direccion', ''),
            telefono=validated_data.get('telefono', ''),
            rol=validated_data.get('rol', 'comprador'),
            puntos=validated_data.get('puntos', 0)
        )
        return user

class PropietarioSerializer(RegistroSerializer):

    class Meta:
        model = Propietario
        fields = RegistroSerializer.Meta.fields

    def validate(self, data):
        if data.get('rol') != 'propietario':
            raise serializers.ValidationError("El rol debe de ser 'propietario' para crear un Propietario")
        return data
    
    def create(self, validated_data):
        if Usuario.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya existe"})
        if Usuario.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Este correo electrónico ya existe"})

        user = Propietario.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # Este método cifrará la contraseña automáticamente
            direccion=validated_data.get('direccion', ''),
            telefono=validated_data.get('telefono', ''),
            rol=validated_data.get('rol', 'comprador'),
        )
        return user

"""
    Para las actualizaciones
"""

class UpdateCompradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprador
        fields = ['first_name', 'last_name', 'direccion', 'telefono']

class UpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ['rol']