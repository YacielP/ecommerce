from rest_framework.permissions import BasePermission

class EsCompradorOPropietario(BasePermission):
    def has_permission(self, request, view):
        # Solo compradores y propietarios de tiendas pueden listar los comentarios
        if request.user.rol == 'comprador':
            return True

        # Verificar si el usuario es propietario de la tienda
        tienda_id = view.kwargs['tienda_id']
        return request.user.tiendas.filter(id=tienda_id).exists()
