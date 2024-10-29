import django_filters
from .models import InventarioProducto

class InventarioProductoFilter(django_filters.FilterSet):
    nombre_producto = django_filters.CharFilter(field_name='producto_central__nombre', lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio_personalizado', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_personalizado', lookup_expr='lte')
    categoria = django_filters.CharFilter(field_name='producto_central__categoria__nombre', lookup_expr='icontains')

    class Meta:
        model = InventarioProducto
        fields = ['nombre_producto', 'precio_min', 'precio_max', 'categoria']
