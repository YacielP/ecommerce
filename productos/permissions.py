from rest_framework.permissions import BasePermission

class IsPropietario(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'propietario'):
            return obj.propietario == request.user
        elif hasattr(obj, 'tienda'):
            return obj.tienda.propietario == request.user
        return False
