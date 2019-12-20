from pdb import set_trace as debug

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from common.decorators import ajax_required

from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    """Create an image."""
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # Assign current user to the image.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            # Redirect user to new created image detail view.
            return redirect(new_item.get_absolute_url())
    else:
        # Initial data is the url and title of an image from an external website as provided by our JavaScript tool.
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

def image_detail(request, id, slug):
    """Display an image's details."""
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


# All requests must be generated via AJAX.
@ajax_required
@login_required
# Only allow POST requests to enter this view.
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # Assume the user wants to 'like' or 'unlike' an image.
            if action == 'like':
                # Indicate that the image is liked by the given user.
                image.users_like.add(request.user)
            else:
                # See Related objects reference
                # https://docs.djangoproject.com/en/dev/ref/models/relations/
                image.user_like.remove(request.user)
            # Return response in JSON format.
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})
