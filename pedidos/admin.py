from django.contrib import admin
from .models import Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ("producto", "cantidad", "precio_unitario")
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "estado", "total", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("id", "usuario__email")
    list_select_related = ("usuario",)
    inlines = [DetallePedidoInline]
    readonly_fields = ("estado", "total", "fecha_creacion")