from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm


# Require a POST since this view changes data.
@require_POST
def cart_add(request, product_id):
    """Add an item to a cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """Remove one or more items from a cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display a cart and its items."""
    cart = Cart(request)
    # Allow user to change the quantity from the details page.
    for item in cart:
        # Remember that a cart is stored as a dictionary in the user's session.
        # Here, we're adding a new key/value pair to the cart.
        # Create an instance of CartAddProductForm for each item in the cart to
        # allow changing product quantities. Initialize the form with the current
        # item quantity and set the update field to True so that when we submit the
        # form to the cart_add view, the current quantity is replaced with the new
        # one.
        # I DON'T QUITE UNDERSTAND WHAT THIS CODE IS DOING.
        item['update_quantity_form'] = CartAddProductForm(
                    initial={'quantity': item['quantity'],
                    'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
