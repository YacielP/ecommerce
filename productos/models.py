from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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

class ProductoCentral(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    tienda = models.OneToOneField(Tienda, on_delete=models.CASCADE, related_name='inventario')

    def __str__(self):
        return f'Inventario de la tienda {self.tienda.nombre}'

class InventarioProducto(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    producto_central = models.ForeignKey(ProductoCentral, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_personalizado = models.FloatField(validators=[MinValueValidator(0.99)])
    resenna = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=0)

    def __str__(self):
        return f'{self.producto_central.nombre} - {self.cantidad} disponible(s) en {self.inventario.tienda.nombre}'
    
