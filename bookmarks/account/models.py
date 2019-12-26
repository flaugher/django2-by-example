from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    """Track when users follow each other.

    The book says this is the way to create a M2M
    relationship that needs additional fields. Then
    add a M2M field to one of the related models (see
    User.add_to_class above) with the 'through'
    parameter.
    See loc. 3658.
    """
    # User who creates the relationship
    user_from = models.ForeignKey('auth.User',
        related_name='rel_from_set',
        on_delete=models.CASCADE)
    # User being followed
    user_to = models.ForeignKey('auth.User',
        related_name='rel_to_set',
        on_delete=models.CASCADE)
    # Create index to improved QuerySet performance.
    created = models.DateTimeField(auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,
            self.user_to)

# Add the following field to User dynamically.
# Note that it must come after 'Contact' since it
# references it.
#
# Enables: user.followers.all() and
# user.following.all().
# 'symmetrical=False' means that if user 1
# follows user 2, it doesn't automatically mean
# that user 2 follows user 1.
User.add_to_class('following',
    models.ManyToManyField('self',
        through=Contact,
        related_name='followers',
        symmetrical=False))


class Profile(models.Model):
    """Extend the User model."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
