from rest_framework import routers, serializers, viewsets
from django.urls import reverse
from .models import Recipe, Ingredient
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ()

class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):
    slugged_url = serializers.URLField(source='get_absolute_url')
    tags = TagListSerializerField()
    ingredients = serializers.StringRelatedField(many=True, read_only=True)
    total_time = serializers.IntegerField(read_only=True)
    avg_ratings = serializers.FloatField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ()

