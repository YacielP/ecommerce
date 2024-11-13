from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Actividad
from logros.models import Logro, LogroTienda, LogroUsuario
from pedidos.models import Pedido
from comentarios.models import Comentario
from productos.models import Tienda

@receiver(post_save, sender=Pedido)
def registrar_compra(sender, instance, created, **kwargs):
    if created:
        user = instance.usuario
        Actividad.objects.create(
            usuario=user,
            tipo="Compra",
            descripcion=f"Realizó un compra en la tienda {instance.tienda.nombre}"
        )
        propietario = instance.tienda.propietario
        Actividad.objects.create(
            usuario=propietario,
            tipo="Venta",
            descripcion=f"Realizó una venta en su tienda {instance.tienda.nombre}"
        )

@receiver(post_save, sender=Comentario)
def registrar_comentario(sender, instance, created, **kwargs):
    if created:
        user = instance.usuario
        Actividad.objects.create(
            usuario=user,
            tipo="Comentario",
            descripcion=f"Realizó un comentario para el producto {instance.inventario_producto.producto_central.nombre} en la tienda {instance.inventario_producto.inventario.tienda.nombre}"
        )

@receiver(post_save, sender=Tienda)
def registrar_tienda(sender, instance, created, **kwargs):
    if created:
        user = instance.propietario
        Actividad.objects.create(
            usuario=user,
            tipo="Apertura de Tienda",
            descripcion=f"Abrió una tienda llamada {instance.nombre}"
        )

def check_order_achievements(user):
    total_orders = Pedido.objects.filter(usuario=user).count()
    logros = {
        "Comprador Novato": 1,
        "Comprador Frecuente": 100
    }

def check_comentario_archievements(user):
    total_comentario = Comentario.objects.filter(usuario=user).count()
    logros = {
        "Reseñador Entusiasta": 10
    }

def check_store_archievements(user):
    total_stores = 