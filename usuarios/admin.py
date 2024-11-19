from django.contrib import admin

from .models import Usuario, Comprador, Propietario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol']

@admin.register(Comprador)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'puntos']

@admin.register(Propietario)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol']