from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos/inventario-producto', views.InventarioProductoViewSet)
router.register(r'tienda', views.TiendaViewSet, basename='tienda')

urlpatterns = [
    path('', include(router.urls)),
    path('tienda/<int:tienda_id>/catalogo/', views.MostrarCatalogoView.as_view(), name='mostrar-catalogo'),
    path('tienda/<int:tienda_id>/agregar/', views.AgregarProductoInventarioView.as_view(), name='agregar-producto'),
    path('tienda/<int:tienda_id>/eliminar/', views.EliminarProductoInventarioView.as_view(), name='eliminar-producto'),
]
