from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Actividad
from logros.models import Logro, LogroTienda, LogroUsuario
from pedidos.models import Pedido
from comentarios.models import Comentario
from productos.models import Tienda

