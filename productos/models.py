from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Usuario
from django.core.exceptions import ValidationError

class Tienda(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    direccion = models.CharField(max_length=200, blank=False, null=False)
    descripcion = models.TextField(null=True, blank=True, default='')
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tiendas', null=False, blank=False)

    # Contamos la variedad de productos. Ej: Producto A=5, Producto B=10, total=2
    def total_productos(self):
        return self.productos.count()

    # Contamos la cantidad total de productos. Ej: Producto A=5, Producto B=10, total=15
    def total_productos(self):
        return self.productos.aggregate(total=models.Sum('cantidad'))['total'] or 0

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Verificar si el propietario tiene el rol "tienda"
        if self.propietario.rol != 'tienda':
            raise ValidationError("El propietario debe tener el rol 'tienda'.")
        super(Tienda, self).save(*args, **kwargs)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    precio = models.FloatField(validators=[MinValueValidator(0.99)], default=0.99)
    descripcion = models.TextField(blank=True, null=True, default='')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos', blank=False, null=False)

    def __str__(self):
        return self.nombre
