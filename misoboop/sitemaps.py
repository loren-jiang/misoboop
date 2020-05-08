# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse
from blog.models import Post
from recipe.models import Recipe

class RecipeSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Recipe.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.modified_at

class BlogSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.modified_at

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about']

    def location(self, item):
        return reverse(item)
