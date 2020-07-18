from decimal import Decimal

from django.conf import settings
from coupons.models import Coupon
from shop.models import Product


class Cart(object):
    """Used to manage the shopping cart."""

    def __init__(self, request):
        """Initialize the cart.

        A cart object is a dictionary that uses a product ID as the
        key and a dictionary with quantity and price as the value for
        each key.

        Cart object:
            { product_id: {quantity, price} }
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """Iterate through items in the card and access related product
        instances."""
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """Add products to a cart or update its quantity."""
        # Convert the product ID to a string because Django uses JSON to serialize session data and JSON only allows string key names.
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as 'modified' to make sure it gets saved."""
        self.session.modified = True

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """Calculate total cost of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def remove(self, product):
        """Remove a product from a cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # howto: use a python property to declare a getter (or setter)
    # See https://www.freecodecamp.org/news/python-property-decorator/
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
