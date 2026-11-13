from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("carrito/", views.CarritoView.as_view(), name="carrito"),
    path("carrito/agregar/<int:pk>/", views.AgregarView.as_view(), name="agregar"),
    path("carrito/actualizar/<int:pk>/", views.ActualizarView.as_view(), name="actualizar"),
    path("carrito/quitar/<int:pk>/", views.QuitarView.as_view(), name="quitar"),
    path("carrito/vaciar/", views.VaciarView.as_view(), name="vaciar"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/confirmar/", views.ConfirmarView.as_view(), name="confirmar"),
    path("<int:pk>/", views.PedidoDetailView.as_view(), name="detalle"),
    path("historial/", views.PedidoListView.as_view(), name="historial"),
    path("<int:pk>/estado/", views.CambiarEstadoView.as_view(), name="cambiar_estado"),
]