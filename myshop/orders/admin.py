import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem

# howto: create custom django admin action
# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/
# Also: https://medium.com/@hakibenita/how-to-add-custom-action-buttons-to-django-admin-8d266f5b0d41


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # Set up response to tell browser to treat is as CSV file.
    response = HttpResponse(content_type='text/csv')

    # Indicate that response contains an attachment.
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name)

    # Create writer object that writes to the response.
    writer = csv.writer(response)

    # Get the model's fields dynamically using get_fields() from its _meta options.
    fields = [field for field in opts.get_fields(
    ) if not field.many_to_many and not field.one_to_many]

    # Write a first row with header information.
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows.
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)

            # Be sure to convert any date objects to strings.
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)
    return response


# Customize the display name.
export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    # Add generic admin action created above to the OrderAdmin class.
    actions = [export_to_csv]
