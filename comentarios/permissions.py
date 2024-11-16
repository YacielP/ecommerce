from rest_framework.permissions import BasePermission

class IsOwnerComentario(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol in ['comprador', 'propietario']
    
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user