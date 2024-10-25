from django.contrib import admin

from .models import Carrito, ItemCarrito, DetallePedido, Pedido

admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(DetallePedido)
admin.site.register(Pedido)
