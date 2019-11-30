from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Comment(models.Model):
    """Stores comments."""
    # Notice how he always creates a related_name for foreign key fields.
    # This names the 'post' attribute for use in specifying the relation
    # from the related object (a post) back to this one.
    # Retrieve the post for a given comment: comment.post
    # Retrieve all comments for a given post: post.comments.all()
    # This is better than having to use 'comment_set'.
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    # Enclose Post in single quotes since it's declared later in the file.
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # Use for deactivating inappropriate comments.
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

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
    """Stores blog posts."""
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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail',
            args=[self.publish.year,
                  self.publish.month,
                  self.publish.day,
                  self.slug
            ]
        )