from rest_framework.permissions import BasePermission

class EsCompradorOPropietario(BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario tiene rol de comprador
        if request.user.rol == 'comprador':
            return True

        # Verificar si el usuario es propietario de la tienda
        tienda_id = view.kwargs['tienda_id']
        return request.user.tiendas.filter(id=tienda_id).exists()

class IsOwner(BasePermission):
    """
    Permiso personalizado para permitir acceso solo a los propietarios de su tienda.
    """

    def has_permission(self, request, view):
        # Verificar si el usuario es propietario de la tienda usando el ID pasado por la URL
        tienda_id = view.kwargs['tienda_id']
        if tienda_id:
            return request.user.tiendas.filter(id=tienda_id).exists()
        return False

    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario es propietario del objeto tienda
        return obj.propietario == request.user
