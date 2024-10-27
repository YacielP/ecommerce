from rest_framework.permissions import BasePermission

class IsCarritoOwner(BasePermission):
    def has_permission(self, request, view):
        # Permiso global: usuario debe estar autenticado
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permiso de objeto: usuario debe ser el propietario del carrito
        return obj.usuario == request.user
