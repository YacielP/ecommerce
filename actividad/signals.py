from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Actividad
from logros.models import Logro, LogroTienda, LogroUsuario
from pedidos.models import Pedido
from comentarios.models import Comentario
from productos.models import Tienda

@receiver(post_save, sender=Pedido)
def registrar_compra_venta(sender, instance, created, **kwargs):
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
        check_order_achievements(user)
        check_venta_archievements(instance.tienda)


@receiver(post_save, sender=Comentario)
def registrar_comentario(sender, instance, created, **kwargs):
    if created:
        user = instance.usuario
        Actividad.objects.create(
            usuario=user,
            tipo="Comentario",
            descripcion=f"Realizó un comentario para el producto {instance.inventario_producto.producto_central.nombre} en la tienda {instance.inventario_producto.inventario.tienda.nombre}"
        )
        check_comentario_archievements(user)

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
    otorgar_logros_usuario(user, total_orders, logros)

def check_comentario_archievements(user):
    total_comentario = Comentario.objects.filter(usuario=user).count()
    logros = {
        "Reseñador Entusiasta": 10
    }
    otorgar_logros_usuario(user, total_comentario, logros)

def check_venta_archievements(tienda):
    total_ventas = Pedido.objects.filter(tienda=tienda).count()
    logros = {
        "Tienda Novata": 1,
        "Superventas": 100
    }
    otorgar_logros_usuario(tienda, total_ventas, logros)

def otorgar_logros_usuario(user, total, logros):
    for logro_name, required in logros.items():
        if total == required:
            logro = Logro.objects.get(nombre=logro_name)
            if not LogroUsuario.objects.filter(usuario=user, logro=logro):
                LogroUsuario.objects.create(
                    usuario=user,
                    logro=logro
                )

def otorgar_logros_tienda(tienda, total, logros):
    for logro_name, required in logros.items():
        if total == required:
            logro = LogroTienda.objects.get(nombre=logro_name)
            if not LogroTienda.objects.filter(tienda=tienda, logro=logro):
                LogroTienda.objects.create(
                    tienda=tienda,
                    logro=logro
                )