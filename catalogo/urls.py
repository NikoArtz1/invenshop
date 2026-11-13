from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.ProductoListView.as_view(), name="lista"),
    path("producto/<int:pk>/", views.ProductoDetailView.as_view(), name="detalle"),
]