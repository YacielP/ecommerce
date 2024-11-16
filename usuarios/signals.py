from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UsuarioComprador
from pedidos.models import Carrito

@receiver(post_save, sender=UsuarioComprador)
def crear_carrito_para_comprador(sender, instance, created, **kwargs):
    if created and instance.rol == 'comprador':
        Carrito.objects.create(usuario=instance)