from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('superuser', 'Superuser'),
        ('tienda', 'Tienda'),
        ('comprador', 'Comprador'),
    ]
    rol = models.CharField(max_length=100, choices=ROL_CHOICES, default='comprador')
    direccion = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
