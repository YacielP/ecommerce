from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioListView, CompradorViewSet, PropietarioViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'propietarios', PropietarioViewSet, basename='propietario')
router.register(r'compradores', CompradorViewSet, basename='comprador')

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario-list'),
    path('rol/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
