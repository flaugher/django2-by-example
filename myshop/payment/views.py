from django.shortcuts import get_object_or_404, redirect, render

import braintree
from orders.models import Order


def payment_process(request):
    """Manage the checkout process."""
    # This order ID was set in the order_create view.
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # Create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            # The nonce will be generated in the template using the Braintree JavaScript SDK.
            'payment_method_nonce': nonce,
            'options': {
                # Automatically submit transaction for settlement.
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # Mark the order as paid
            order.paid = True
            # Store the unique transaction id returned by the Braintree gateway.
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Generate token
        # The Braintree JS SDK will use this token to generate a nonce that will be passed back in the POST.
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token
                       })


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
