from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Image(models.Model):
    """Store images bookmarked from other websites."""
    # A user can post multiple images but each image is posted by only one user.
    # If the user is deleted, delete all their images.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='images_created',
        on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # SEO-friendly URL
    slug = models.SlugField(max_length=200, blank=True)
    # Original URL for where the user saw the image
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    # Create a database index for the created field.
    created = models.DateField(auto_now_add=True, db_index=True)
    # Related field allows you to:
    # Retrieve all users that like an image: image.users_like.all()
    # Retrieve all images liked by a user: user.images_liked.all()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='images_liked',
        blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Automatically generate image slug from the title.

        Only do this when a slug isn' provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)