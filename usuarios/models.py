from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('superuser', 'Superuser'),
        ('propietario', 'Propietario'),
        ('comprador', 'Comprador'),
    ]
    rol = models.CharField(max_length=100, choices=ROL_CHOICES, default='comprador')
    direccion = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('username', 'email')

    def __str__(self):
        return self.username

class Comprador(Usuario):
    puntos = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.rol != 'comprador':
            raise ValueError("El rol debe de ser 'comprador' para un Comprador")
        super().save(*args, **kwargs)

class Propietario(Usuario):
    
    def save(self, *args, **kwargs):
        if self.rol != 'propietario':
            raise ValueError("El rol debe de ser 'tienda' para un Propietario")
        super().save(*args, **kwargs)