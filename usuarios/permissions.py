from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsUsuarioTienda(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'propietario'

class EsUsuarioComprador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'comprador'

    
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj == request.user:
            return True
        
class IsAdminOrPropieratio(BasePermission):
    def has_permission(self, request, view):
        #Verificar si el usuario es administrador o propietario
        return request.user.is_staff or request.user.rol == 'propietario'
    
class IsOwnerOrAdminOrPropietario(BasePermission):
    def has_object_permission(self, request, view, obj):
        #Permitir solo metodos seguros
        if request.method is SAFE_METHODS:
            return request.user.is_staff or obj == request.user or request.user.rol == 'propietario'
        #Permitir solo a los admins y a los propios usuarios eliminar o editar
        return request.user.is_staff or obj == request.user
        