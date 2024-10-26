from django.urls import path
from .views import AgregarAlCarritoView, EliminarDelCarritoView, RealizarPedidoView

urlpatterns = [
    path('tienda/<int:tienda_id>/carrito/agregar/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('tienda/<int:tienda_id>/carrito/eliminar/', EliminarDelCarritoView.as_view(), name='eliminar_del_carrito'),
    path('pedido/realizar/', RealizarPedidoView.as_view(), name='realizar_pedido'),
]
