from rest_framework.permissions import BasePermission

class EsUsuarioTienda(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'tienda'

class EsUsuarioComprador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'comprador'

    
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj == request.user:
            return True