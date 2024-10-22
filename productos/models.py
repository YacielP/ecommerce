from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Usuario

class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True, default='')
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tiendas')

    #Contamos la variedad de productos. Ej: Producto A=5, Producto B=10, total=2
    """
        Esto es pq quiero implementar logros en la aplicacion
    """
    def total_productos(self):
        return self.productos.count()
    
    #Contamos la cantidad total de productos. Ej: Producto A=5, Producto B=10, total=15
    def total_productos(self):
        return self.productos.aggregate(total=models.Sum('cantidad'))['total'] or 0
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, default='')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre
