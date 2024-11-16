from django.db import models
from usuarios.models import UsuarioComprador
from productos.models import InventarioProducto, Tienda
from django.utils import timezone

"""
Carrito e ItemCarrito representan un estado temporal
donde los productos se almacenan antes de confirmar la compra
"""
class Carrito(models.Model):
    usuario = models.OneToOneField(UsuarioComprador, on_delete=models.CASCADE, related_name='carrito')
    
    """
        Para mas adelante mejorar la funcionalidad de RealizarPedido,
        que se puedan crear varios pedidos de diferentes tiendas y asi
        calcular el total
    """
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
    def __str__(self):
        return f'Carrito de {self.usuario.username}'
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    inventario_producto = models.ForeignKey(InventarioProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Nuevo ItemCarrito
            if self.cantidad <= self.inventario_producto.cantidad:
                self.inventario_producto.cantidad -= self.cantidad
                self.inventario_producto.save()
                self.subtotal = self.inventario_producto.precio_personalizado * self.cantidad
                super().save(*args, **kwargs)
            else:
                raise ValueError("Cantidad no disponible en inventario")
        else:  # ItemCarrito existente
            original = ItemCarrito.objects.get(pk=self.pk)
            cantidad_diferencia = self.cantidad - original.cantidad
            if cantidad_diferencia > 0:  # Si se está incrementando
                if cantidad_diferencia <= self.inventario_producto.cantidad:
                    self.inventario_producto.cantidad -= cantidad_diferencia
                    self.inventario_producto.save()
                    self.subtotal = self.inventario_producto.precio_personalizado * self.cantidad
                    super().save(*args, **kwargs)
                else:
                    raise ValueError("Cantidad no disponible en inventario")
            elif cantidad_diferencia < 0:  # Si se está reduciendo
                self.inventario_producto.cantidad -= cantidad_diferencia  # Añadir de vuelta al inventario
                self.inventario_producto.save()
                self.subtotal = self.inventario_producto.precio_personalizado * self.cantidad
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.inventario_producto.cantidad += self.cantidad  # Devolver la cantidad al inventario
        self.inventario_producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad} x {self.inventario_producto.producto_central.nombre}'



"""
Pedido y detallePedido representan una compra finalizada que registra información
esencial del pedido
"""
class Pedido(models.Model):
    usuario = models.ForeignKey(UsuarioComprador, on_delete=models.CASCADE)
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
    inventario_producto = models.ForeignKey(InventarioProducto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.inventario_producto.precio_personalizado * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad} x {self.inventario_producto.producto_central.nombre}'
