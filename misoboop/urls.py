"""misoboop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from recipe import views as recipe_views
from recipe import views_api as recipe_views_api
from rest_framework import routers
from recipe.views import search_recipes
from filebrowser.sites import site
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap, RecipeSitemap

router = routers.DefaultRouter()
# 'recipe-api' is base name to avoid namespace conflicts with 'recipe.urls'
router.register(r'recipes', recipe_views_api.RecipeViewSet, 'recipe-api')
router.register(r'ingredients', recipe_views_api.IngredientViewSet, 'ingredient-api')
router.register(r'tags', recipe_views_api.TagViewset, 'tag-api')

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'recipe': RecipeSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('', recipe_views.home, name='home'),
    path('about/', recipe_views.about, name='about'),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('tinymce/', include('tinymce.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('recipes/', include('recipe.urls')),
    path('blogs/', include('blog.urls')),
    path('api/ingredients_list/', recipe_views_api.IngredientList.as_view()),
    path('api/recipes_list/', recipe_views_api.RecipeList.as_view()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      # url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
