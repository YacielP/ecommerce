from django.db import models
from productos.models import InventarioProducto
from usuarios.models import Usuario

class Comentario(models.Model):
    inventario_producto = models.ForeignKey(InventarioProducto, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} sobre {self.inventario_producto.producto_central.nombre} en {self.inventario_producto.inventario.tienda.nombre}'
