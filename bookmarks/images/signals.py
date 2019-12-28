from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """Update an image's total likes when a user likes it.

    users_like is a ManyToManyField so we send a m2m_changed signal
    to this receiver function.  It updates the total_likes field
    for an image instance when that image's like count changes.

    Saying "@receiver(m2m_changed...)" connects this users_like_changed
    receiver function to the m2m_changed signal.  Note that you still have
    to register this signal in the application configuration class.
    """
    instance.total_likes = instance.users_like.count()
    instance.save()
