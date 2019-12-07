from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    """Create a Post sitemap.

    Usage: 127.0.0.1:8000/sitemap.xml/

    Edit in admin: http://127.0.0.1:8000/admin/sites/site/
    """
    # Attributes that will appear in the sitemap.
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        """Attribute that will appear in sitemap."""
        return obj.updated