from .cart import Cart


def cart(request):
    """Add current cart to the request context."""
    return {'cart': Cart(request)}