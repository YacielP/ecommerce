from django.contrib import admin

from .models import ProductoCentral, Tienda, Inventario, InventarioProducto

admin.site.register(ProductoCentral)
admin.site.register(Tienda)
admin.site.register(InventarioProducto)
admin.site.register(Inventario)
