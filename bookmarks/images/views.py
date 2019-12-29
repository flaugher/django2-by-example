from pdb import set_trace as debug
import redis

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required

from .forms import ImageCreateForm
from .models import Image

# Connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)
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
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')

            # Redirect user to new created image detail view.
            return redirect(new_item.get_absolute_url())
    else:
        # Initial data is the url and title of an image from an external website as provided by our JavaScript tool.
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

def image_detail(request, id, slug):
    """Display an image's details.

    Store the number of times an image is viewed in Redis.
    Redis key notation is "object-type:id:field".
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increment total image views by 1
    total_views = r.incr('image:{}:views'.format(image.id))
    return render(request, 'images/image/detail.html',
                  {'section': 'images',
                  'image': image,
                  'total_views': total_views})


# All requests must be generated via AJAX.
@ajax_required
@login_required
# Only allow POST requests to enter this view.
@require_POST
def image_like(request):
    """A user likes an image."""
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # Assume the user wants to 'like' or 'unlike' an image.
            if action == 'like':
                # Indicate that the image is liked by the given user.
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                # See Related objects reference
                # https://docs.djangoproject.com/en/dev/ref/models/relations/
                image.user_like.remove(request.user)
            # Return response in JSON format.
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})
