from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComentarioViewSet

router = DefaultRouter()
router.register(
    r'tienda/(?P<tienda_id>\d+)/producto/(?P<inventario_producto_id>\d+)/comentarios', 
    ComentarioViewSet, 
    basename='comentarios'
)

urlpatterns = [
    path('', include(router.urls)),
]
