from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    """Create new Action objects in a simple way."""
    action = Action(user=user, verb=verb, target=target)
    action.save()