from django.db.models.signals import post_save
from django.dispatch import receiver
from productos.models import Inventario, Tienda

@receiver(post_save, sender=Tienda)
def crear_inventario_para_tienda(sender, instance, created, **kwargs):
    if created:  # Verifica si la instancia fue creada
        Inventario.objects.create(tienda=instance)