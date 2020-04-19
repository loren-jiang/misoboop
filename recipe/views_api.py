from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters
from rest_framework import permissions
from .serializers import RecipeSerializer, IngredientSerializer
from .models import Recipe, Ingredient
from rest_framework.views import APIView
from rest_framework.response import Response
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from .filters import RecipeFilterSet

class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited if Admin User
    """
    queryset = Recipe.objects.prefetch_related('ingredients', 'tags').order_by('likes')
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilterSet

        # permission_classes = [permissions.IsAdminUser]

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited if Admin User
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
        # permission_classes = [permissions.IsAdminUser]

class IngredientList(APIView):
    """
    List all ingredients.
    """
    def get(self, request, format=None):
        qs = Ingredient.objects.all()
        serializer = IngredientSerializer(qs, many=True)
        return Response(serializer.data)

class RecipeList(APIView):
    """
    List all ingredients.
    """
    def get(self, request, format=None):
        qs = Recipe.objects.prefetch_related('ingredients', 'tags').order_by('likes')
        # qs = Recipe.objects.all()
        serializer = RecipeSerializer(qs, many=True)
        return Response(serializer.data)

class TagViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TaggitSerializer