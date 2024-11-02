from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'inventario-producto', views.InventarioProductoViewSet)

urlpatterns = [
    path('', views.TiendaListView.as_view(), name='tienda-list'),
    path('productos/', include(router.urls)),
    path('create/', views.TiendaCreateView.as_view(), name='tienda-create'),
    path('tienda/<int:tienda_id>/', views.TiendaDetailView.as_view(), name='tienda-detail'),
    path('tienda/<int:tienda_id>/catalogo/', views.MostrarCatalogoView.as_view(), name='mostrar-catalogo'),
    path('tienda/<int:tienda_id>/agregar/', views.AgregarProductoInventarioView.as_view(), name='agregar-producto'),
    path('tienda/<int:tienda_id>/eliminar/', views.EliminarProductoInventarioView.as_view(), name='eliminar-producto'),
]
