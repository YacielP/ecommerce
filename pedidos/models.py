from django.db import models
from usuarios.models import Usuario
from productos.models import Producto, Tienda
from django.utils import timezone

"""
Carrito e ItemCarrito representan un estado temporal
donde los productos se almacenan antes de confirmar la compra
"""
class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carrito')

    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
    def __str__(self):
        return f'Carrito de {self.usuario.username}'
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.FloatField()

    def save(self, *args, **kwargs):
        self.subtotal = self.producto * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

"""
Representa una compra finalizada que registra información
esencial del pedido
"""
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()

    def __str__(self):
        return f'Pedido {self.id} de {self.usuario}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'