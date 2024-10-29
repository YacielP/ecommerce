from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'inventario-producto', views.InventarioProductoViewSet)

urlpatterns = [
    path('', views.TiendaListView.as_view(), name='tienda-list'),
    path('productos/', include(router.urls)),
    path('create/', views.TiendaCreateView.as_view(), name='tienda-create'),
    path('tienda/<int:pk>/', views.TiendaDetailView.as_view(), name='tienda-detail'),
    path('tienda/<int:pk>/catalogo/', views.MostrarCatalogoView.as_view(), name='mostrar-catalogo'),
    path('producto/create/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('producto/<int:pk>/', views.ProductDetailView.as_view(), name='producto-detail'),
    path('tienda/<int:pk>/agregar/', views.AgregarProductoInventarioView.as_view(), name='agregar-producto'),
    path('tienda/<int:pk>/eliminar/', views.EliminarProductoInventarioView.as_view(), name='eliminar-producto'),
]
