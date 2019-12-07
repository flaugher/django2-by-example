from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):
    """RSS feed that serves up latest blog posts.

    Usage: http://127.0.0.1/blog/feed/
    """
    # Attributes that correspond to typical RSS elements
    title = 'My blog'
    link = '/blog/'
    description = 'New posts from my blog.'

    def items(self):
        """Retrieve the last five objects to be included in the feed."""
        return Post.published.all()[:5]

    def item_title(self, item):
        """Return the title for each object."""
        return item.title

    def item_description(self, item):
        """Return the description for each object."""
        return truncatewords(item.body, 30)
