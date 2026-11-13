from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PAGADO = "PAGADO", "Pagado"
        ENVIADO = "ENVIADO", "Enviado"
        CANCELADO = "CANCELADO", "Cancelado"
        
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    estado = models.CharField(
        max_length=10, choices = Estado.choices, default=Estado.PENDIENTE
    )
    
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=10)
    telefono_contacto = models.CharField(max_length=30)
    
    class Meta:
        ordering = ["-fecha_creacion"]

    TRANSICIONES = {
        Estado.PENDIENTE: [Estado.PAGADO, Estado.CANCELADO],
        Estado.PAGADO: [Estado.ENVIADO, Estado.CANCELADO],
        Estado.ENVIADO: [],
        Estado.CANCELADO: [],
    }

    def estados_siguientes(self):
        #Devuelve los estados a los que puede pasar
        return [(e.value, e.label) for e in self.TRANSICIONES.get(self.estado, [])]
    
    def __str__(self):
        return f"Pedido #{self.pk} - {self.usuario}"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="detalles"
    )
    
    producto = models.ForeignKey(
        "catalogo.Producto", on_delete=models.PROTECT
    )
    
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "detalle de pedido"
        verbose_name_plural = "detalles de pedido"
        
    def __str__(self):
        return f"{self.cantidad} x {self.producto}"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario