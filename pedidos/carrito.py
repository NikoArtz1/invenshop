from decimal import Decimal

from catalogo.models import Producto

class Carrito:
    SESSION_KEY = "carrito"

    def __init__(self, request):
        self.session = request.session
        self.items = self.session.setdefault(self.SESSION_KEY, {})
        self._lineas = None


    def agregar(self, producto, cantidad=1):
        if cantidad < 1:
            raise ValueError("La cantidad debe ser al menos 1.")
        if not producto.activo:
            raise ValueError("Este producto no está disponible.")
        pid = str(producto.pk)
        nueva = self.items.get(pid, 0) + cantidad
        self._validar_stock(producto, nueva)
        self.items[pid] = nueva
        self._guardar()

    def actualizar(self, producto, cantidad):
        if cantidad < 1:
            self.quitar(producto)
            return
        self._validar_stock(producto, cantidad)
        self.items[str(producto.pk)] = cantidad
        self._guardar()

    def quitar(self, producto):
        self.items.pop(str(producto.pk), None)
        self._guardar()

    def vaciar(self):
        self.session[self.SESSION_KEY] = {}
        self.items = self.session[self.SESSION_KEY]
        self._guardar()


    def lineas(self):
        if self._lineas is None:
            ids = [int(pid) for pid in self.items]
            productos = Producto.objects.filter(pk__in=ids, activo=True).select_related("categoria")
            por_id = {p.pk: p for p in productos}

            lineas = []
            for pid in list(self.items):
                producto = por_id.get(int(pid))
                if producto is None:            # borrado o desactivado desde que se agregó
                    del self.items[pid]
                    self._guardar()
                    continue
                cantidad = self.items[pid]
                lineas.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "subtotal": producto.precio * cantidad,
                    "disponible": cantidad <= producto.stock,
                })
            self._lineas = lineas
        return self._lineas

    @property
    def total(self):
        return sum((l["subtotal"] for l in self.lineas()), Decimal("0"))

    def __len__(self):
        return sum(self.items.values())


    def _validar_stock(self, producto, cantidad):
        if producto.stock == 0:
            raise ValueError(f"«{producto.nombre}» está agotado.")
        if cantidad > producto.stock:
            raise ValueError(f"Solo hay {producto.stock} unidades de «{producto.nombre}».")

    def _guardar(self):
        self.session.modified = True
        self._lineas = None