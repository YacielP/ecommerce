from rest_framework.permissions import BasePermission

class EsUsuarioTienda(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'tienda'

class EsUsuarioComprador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'comprador'

    
class IsDuenno(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user