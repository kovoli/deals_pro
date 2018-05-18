from django.contrib.sitemaps import Sitemap
from .models import Deal, Store


class DealSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Deal.objects.all()

    def lastmod(self, obj):
        return obj.publish


class StoreSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Store.objects.all()

    def lastmod(self, obj):
        return obj.publish
