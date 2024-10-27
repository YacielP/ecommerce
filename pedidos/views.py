from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from productos.models import ProductoCentral, InventarioProducto
from .models import Carrito, ItemCarrito, Pedido, DetallePedido
from .permissions import IsCarritoOwner
from usuarios.permissions import EsUsuarioComprador

class AgregarAlCarritoView(APIView):
    permission_classes = [IsCarritoOwner, EsUsuarioComprador]

    def post(self, request, tienda_id):
        usuario = request.user
        nombre_producto = request.data.get('nombre_producto')
        producto = InventarioProducto.objects.get(inventario__tienda__id=tienda_id, producto_central__nombre=nombre_producto)
        carrito, created = Carrito.objects.get_or_create(usuario=usuario)

        self.check_object_permissions(request, carrito)

        item_carrito, created_item_carrito = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            inventario_producto=producto,
            defaults={'cantidad': int(request.data.get('cantidad', 1))}
        )

        if not created_item_carrito:
            item_carrito.cantidad += int(request.data.get('cantidad', 1))
            item_carrito.save()

        return Response({'message': 'Producto añadido al carrito'}, status=status.HTTP_201_CREATED)

    
class EliminarDelCarritoView(APIView):
    permission_classes = [IsCarritoOwner, EsUsuarioComprador]

    def delete(self, request, tienda_id):
        usuario = request.user
        nombre_producto = request.data.get('nombre_producto')
        cantidad_a_eliminar = int(request.data.get('cantidad', 1))

        producto = InventarioProducto.objects.get(inventario__tienda__id=tienda_id, producto_central__nombre=nombre_producto)
        carrito = Carrito.objects.get(usuario=usuario)

        self.check_object_permissions(request, carrito)

        item_carrito = ItemCarrito.objects.filter(carrito=carrito, inventario_producto=producto).first()

        if item_carrito:
            if item_carrito.cantidad > cantidad_a_eliminar:
                item_carrito.cantidad -= cantidad_a_eliminar
                item_carrito.save()
                return Response({'message': 'Producto actualizado del carrito'}, status=status.HTTP_200_OK)
            elif item_carrito.cantidad == cantidad_a_eliminar:
                item_carrito.delete()
                return Response({'message': 'Producto eliminado del carrito'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'La cantidad que desea eliminar es mayor que la cantidad real'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)
        
class RealizarPedidoView(APIView):
    def post(self, request, *args, **kwargs):
        usuario = request.user
        carrito = Carrito.objects.get(usuario=usuario)
        if not carrito.items.exists():
            return Response({'error': 'El carrito está vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            pedido = Pedido.objects.create(
                usuario=usuario,
                tienda=carrito.items.first().inventario_producto.inventario.tienda
            )
            for item in carrito.items.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    inventario_producto=item.inventario_producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal
                )
            pedido.calcular_total()
            carrito.items.all().delete()

        return Response({'message': 'Pedido realizado con éxito.'}, status=status.HTTP_201_CREATED)