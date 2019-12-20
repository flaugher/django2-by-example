from django.http import HttpResponseBadRequest


def ajax_required(f):
    """Decorator that restricts AJAX views to allow only requests generated via AJAX.

    Usage: @ajax_required
           def foobar(request):
               pass
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
