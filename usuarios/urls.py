from django.urls import path
from .views import UsuarioListView, UsuarioCreateView, UsuarioDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario-list'),
    path('registrar/', UsuarioCreateView.as_view(), name='usuario-create'),
    path('usuario/<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
