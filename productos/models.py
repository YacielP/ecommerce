from django.db import models
from usuarios.models import Usuario

#FALTA TRABAJAR AQUI PARA REDUCIR EL INVENTARIO CUANDO SE ELIMINE UN PRODUCTO

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.nombre

class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True, default='')
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tiendas')

    def total_productos(self):
        return self.inventarios.aggregate(total=models.Sum('cantidad'))['total'] or 0
    
    def cantidad_producto_especifico(self, producto_id):
        return self.inventarios.filter(producto_id=producto_id).aggregate(total=models.Sum('cantidad'))['total'] or 0

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='inventarios')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.producto.nombre} - {self.tienda.nombre}'

