from pdb import set_trace as debug

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


@staff_member_required
def admin_order_detail(request, order_id):
    # howto: render a detail view page
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def order_create(request):
    """Create a new order."""
    # debug()
    # Get current cart from the session.
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create new order in database but don't save it at first.  Wait and apply a
            # coupon, if there is one, and then save the order.
            # howto: create an object without saving it
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # Launch async task
            order_created.delay(order.id)

            # Set the order in the session
            request.session['order_id'] = order.id

            # Redirect to payment
            return redirect(reverse('payment:process'))

            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
