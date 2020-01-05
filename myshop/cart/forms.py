from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    """Form for adding a product to a cart."""
    # Users can select a quantity between 1 and 20.
    # TypedChoiceField + coerce ensure input is converted to an integer.
    quantity = forms.TypedChoiceField(
                        choices=PRODUCT_QUANTITY_CHOICES,
                        coerce=int)
    # False -> No existing quantity has to be updated.
    # True -> Update an existing quantity with input quantity.
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)