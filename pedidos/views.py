from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Carrito, ItemCarrito, Pedido, DetallePedido
from productos.models import Producto
from django.db import transaction

class AgregarAlCarritoView(APIView):
    def post(self, request, producto_id):
        usuario = request.user
        producto = Producto.objects.get(id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=usuario)
        item_carrito, created_item_carrito = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': request.data.get('cantidad', 1)}
        )
        if not created_item_carrito:
            item_carrito.cantidad += int(request.data.get('cantidad', 1))
            item_carrito.save()
        
        return Response({'message': 'Producto añadido al carrito'}, status=status.HTTP_201_CREATED)
    
class EliminarDelCarritoView(APIView):
    def delete(self, request, producto_id):
        usuario = request.user
        producto = Producto.objects.get(id=producto_id)
        carrito = Carrito.objects.get(usuario=usuario)
        item_carrito = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        if item_carrito:
            cantidad_a_eliminar = int(request.data.get('cantidad', 1))
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
            return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            pedido = Pedido.objects.create(
                usuario=usuario,
                tienda=carrito.items.first().producto.tienda
            )
            for item in carrito.items.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal
                )
            pedido.calcular_total()
            carrito.items.all().delete()

        return Response({'message': 'Pedido realizado con éxito'}, status=status.HTTP_201_CREATED)