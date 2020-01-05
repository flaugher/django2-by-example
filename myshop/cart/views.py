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

def cart_remove(request):
    """Remove one or more items from a cart."""
    cart = cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display a cart and its items."""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
