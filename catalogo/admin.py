from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}   
    search_fields = ("nombre",)
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "activo")
    list_editable = ("stock", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "descripcion")
    list_select_related = ("categoria",)