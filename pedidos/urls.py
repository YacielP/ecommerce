from django.urls import path
from .views import AgregarAlCarritoView, EliminarDelCarritoView, RealizarPedidoView

urlpatterns = [
    path('carrito/agregar/<int:producto_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', EliminarDelCarritoView.as_view(), name='eliminar_del_carrito'),
    path('pedido/realizar/', RealizarPedidoView.as_view(), name='realizar_pedido'),
]
