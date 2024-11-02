from rest_framework.permissions import BasePermission

class IsCarritoOwner(BasePermission):
    def has_permission(self, request, view):
        # Permiso global: usuario debe ser comprador
        return request.user.rol == 'comprador'

    def has_object_permission(self, request, view, obj):
        # Permiso de objeto: usuario debe ser el propietario del carrito
        return obj.usuario == request.user
