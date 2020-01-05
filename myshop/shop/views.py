from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_detail(request, id, slug):
    """Display a single product."""
    # Also get the slug so we can build an SEO-friendly URL for the product.
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

def product_list(request, category_slug=None):
    """Display products."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
