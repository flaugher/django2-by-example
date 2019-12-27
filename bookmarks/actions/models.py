from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    """Track what users do on the platform."""
    user = models.ForeignKey('auth.User',
        related_name='actions',
        db_index=True,
        on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    # Points to another model
    # You can limit models with limit_choices_to attribute.
    target_ct = models.ForeignKey(ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    # Points to instance of that model
    target_id = models.PositiveIntegerField(null=True,
        blank=True,
        db_index=True)
    # The two properties above, taken together, describe the action a user took.
    # These two fields have 'blank=True, null=True' so that a target object
    # isn't required when saving Action objects.  This allows the admin to
    # define new actions before they are actually associated with any users.

    # This field doesn't actually appear in the database.
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)
