from decimal import Decimal
from django.db import transaction
from django.db.models import F
from catalogo.models import Producto
from .models import DetallePedido, Pedido


class PedidoError(Exception):
    "El error se le muestra al usuario"


@transaction.atomic
def crear_pedido(usuario, carrito, datos_envio):
    items = {int(pid): cantidad for pid, cantidad in carrito.items.items()}
    if not items:
        raise PedidoError("El carrito está vacío.")

    # Bloquea las filas de los productos hasta que termine la transacción
    productos = (
        Producto.objects.select_for_update()
        .filter(pk__in=items)
        .order_by("pk")
    )
    por_id = {p.pk: p for p in productos}

    pedido = Pedido.objects.create(usuario=usuario, **datos_envio)

    detalles = []
    total = Decimal("0")
    for pid, cantidad in items.items():
        producto = por_id.get(pid)
        if producto is None or not producto.activo:
            raise PedidoError("Uno de los productos ya no está disponible.")
        if cantidad > producto.stock:
            raise PedidoError(
                f"Stock insuficiente de «{producto.nombre}» (quedan {producto.stock})."
            )

        producto.stock -= cantidad
        producto.save(update_fields=["stock"])

        detalles.append(
            DetallePedido(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )
        )
        total += producto.precio * cantidad

    DetallePedido.objects.bulk_create(detalles)
    pedido.total = total
    pedido.save(update_fields=["total"])
    return pedido


@transaction.atomic
def cambiar_estado(pedido_id, nuevo_estado):
    pedido = Pedido.objects.select_for_update().get(pk=pedido_id)

    permitidos = [e.value for e in Pedido.TRANSICIONES.get(pedido.estado, [])]
    if nuevo_estado not in permitidos:
        raise PedidoError(
            f"No se puede cambiar un pedido «{pedido.get_estado_display()}» a ese estado."
        )

    if nuevo_estado == Pedido.Estado.CANCELADO:
        for detalle in pedido.detalles.all():
            Producto.objects.filter(pk=detalle.producto_id).update(
                stock=F("stock") + detalle.cantidad
            )

    pedido.estado = nuevo_estado
    pedido.save(update_fields=["estado"])
    return pedido