from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        """Create custom manager.

        This allows us to define a new 'published' queryset attribute on the Post model
        that displays published posts.  We can then apply various filters to this custom queryset.
        """
        queryset = super(PublishedManager, self).get_queryset()
        queryset = queryset.filter(status='published')
        return queryset

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # Use unique_for_date to build URLs for posts using their publish date and the slug.
    # This prevents multiple posts from having the same slug for a given date.
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()          # The default manager
    published = PublishedManager()      # Our custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog:post_detail,
            args=[self.publisher.year,
                  self.publisher.month,
                  self.publisher.day,
                  self.slug
            ]
        )