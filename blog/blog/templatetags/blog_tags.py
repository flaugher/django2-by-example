from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from ..models import Post


# Use template tags to process data and add it to any template
# regardless of the view being executed. Restart the web server
# any time you add a new tags file.

# This module needs this 'register' variable to be a valid tag library.
register = template.Library()

@register.simple_tag
def get_most_commented_posts(count=5):
    """Get the most commented posts."""
    # Aggregate the total number of comments for each post.  Return a query set that
    # stores the total number of comments for each post in the 'total_comments' computed field.
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.simple_tag
def total_posts():
    """Retrieve total posts published in the blog."""
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Show latests number of published posts.

    Usage: {% show_latest_posts COUNT}
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    # Inclusion tags have to return a dictionary of values.
    return {'latest_posts': latest_posts}

@register.filter(name='markdown')
def markdown_format(text):
    """Enable use of markdown syntax in blog posts.

    Name function 'markdown_format' to avoid name collision when we do
    {{ variable|markdown }} in templates.

    mark_safe marks the result as safe HTML so Django doesn't escape it
    when outputting it.
    """
    return mark_safe(markdown.markdown(text))