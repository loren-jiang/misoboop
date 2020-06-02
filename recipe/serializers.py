from rest_framework import routers, serializers, viewsets
from django.urls import reverse
from .models import Recipe, Ingredient, IngredientAmount, Unit, BasicTag
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from core.serializers import PublicImageSerializer

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ()



class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):
    slugged_url = serializers.URLField(source='get_absolute_url')
    tags = TagListSerializerField()
    ingredients = serializers.StringRelatedField(many=True, read_only=True)
    image = PublicImageSerializer(read_only=True)
    total_time = serializers.IntegerField(read_only=True)
    avg_ratings = serializers.FloatField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ()

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('name', 'name_abbrev', 'type', 'system',)

class IngredientAmountSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    class Meta:
        model = IngredientAmount
        exclude= ()

class BasicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicTag
        exclude = ()
