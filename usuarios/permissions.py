from rest_framework.permissions import BasePermission

class EsUsuarioTienda(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'tienda'

class EsUsuarioComprador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'comprador'

    
class IsDuenno(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'inventario'):
            return obj.inventario.tienda.propietario == request.user
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user