from django.db import models
from usuarios.models import UsuarioComprador
from productos.models import Tienda

class Logro(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    puntos = models. PositiveIntegerField()
    beneficio = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class LogroUsuario(models.Model):
    usuario = models.ForeignKey(UsuarioComprador, on_delete=models.CASCADE)
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtenido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.logro.nombre}'
    
class LogroTienda(models.Model):
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtenido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tienda.nombre} - {self.logro.nombre}'