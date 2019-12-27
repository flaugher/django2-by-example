import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action


def create_action(user, verb, target=None):
    """Create new Action objects.

    target is a model class.

    Also prevent website from storing the same action from the same user in short amounts of time.

    Actions:
    - A user bookmarks an image.
    - A user likes an image.
    - A user creates an account.
    - A user starts following another user.
    """
    # Check for similar actions made in the last minute.
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    # Find similar actions created one minute ago or longer.
    similar_actions = Action.objects.filter(user_id=user.id,
        verb=verb,
        created__gte=last_minute)

    # I don't understand this logic.  Shouldn't we filter on 'created__lt=last_minute'?
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
            target_id=target_id)

    if not similar_actions:
        # Create an Action object if no identical action already exists in the last minute.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
