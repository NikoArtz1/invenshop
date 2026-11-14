from django.contrib import admin

from .models import DetallePedido, Pedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    can_delete = False
    readonly_fields = ("producto", "cantidad", "precio_unitario")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "estado", "total", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("id", "usuario__email")
    list_select_related = ("usuario",)
    readonly_fields = ("usuario", "estado", "total", "fecha_creacion")
    inlines = [DetallePedidoInline]