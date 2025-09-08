from django.urls import reverse
from django.contrib.sitemaps import Sitemap
    

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'mulai-jelajah']

    def location(self, item):
        return reverse(item)

