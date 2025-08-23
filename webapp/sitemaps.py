from django.contrib.sitemaps import Sitemap
from .models import Property, About


class PropertySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Property.objects.filter(is_active_new=True)

    def lastmod(self, obj):
        return obj.date_posted

    def location(self, obj):
        return f"/property/{obj.slug}/"


class AboutSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return About.objects.all()

    def location(self, obj):
        return "/about/"
