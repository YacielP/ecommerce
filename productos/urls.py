from django.urls import path
from . import views

urlpatterns = [
    path('', views.TiendaListView.as_view(), name='tienda-list'),
    path('create/', views.TiendaCreateView.as_view(), name='tienda-create'),
    path('tienda/<int:pk>/', views.TiendaDetailView.as_view(), name='tienda-detail'),
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('producto/create/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('producto/<int:pk>/', views.ProductDetailView.as_view(), name='producto-detail'),
]
