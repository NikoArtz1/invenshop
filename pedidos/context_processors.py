def carrito(request):
    items = request.session.get("carrito", {})
    return {"carrito_cantidad": sum(items.values())}