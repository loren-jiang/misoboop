from django.urls import path, re_path

from .views import RecipeDetailView, RecipeListView, like_recipe

urlpatterns = [
    path('<slug:slug>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('', RecipeListView.as_view(), name='recipe-list'),
    path('<slug:slug>/like', like_recipe, name='like-recipe'),
]