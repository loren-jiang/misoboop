from django.urls import path, re_path
from .views import RecipeSeriesListView, RecipeDetailView, RecipeListView, ExploreRecipesListView, like_recipe, \
    search_recipes, \
    explore_recipes, tagged_by_recipes, RecipeSeriesDetailView

urlpatterns = [
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe-detail'),
    # path('', RecipeListView.as_view(), name='recipe-list'),
    path('', search_recipes, name='recipe-list'),
    path('tag/<slug:slug>/', tagged_by_recipes, name='tagged-by-recipes'),
    path('recipe/<slug:slug>/like/', like_recipe, name='like-recipe'),
    path('search/', search_recipes, name='search-recipes'),
    path('explore/', explore_recipes, name='explore-recipes'),
    path('series/', RecipeSeriesListView.as_view(), name='series-list'),
    path('series/<slug:slug>/', RecipeSeriesDetailView.as_view(), name='series-detail'),
]
