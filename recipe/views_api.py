from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters
from rest_framework import permissions
from .serializers import RecipeSerializer, IngredientSerializer
from .models import Recipe, Ingredient
from rest_framework.views import APIView
from rest_framework.response import Response
from taggit.models import Tag
from taggit_serializer.serializers import TaggitSerializer
from .filters import RecipeFilterSet, NullsAlwaysLastOrderingFilter
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data,
            'page_size': self.page_size,
            'current_page': self.page.number,
        })


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 400
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited if Admin User
    """
    queryset = Recipe.objects.prefetch_related('ingredients', 'tags') \
        .annotate(total_time=F('cook_time') + F('prep_time')) \
        .annotate(avg_ratings=F('ratings__average'))
    # pagination_class = CustomPagination
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilterSet
    filter_backends = [DjangoFilterBackend, NullsAlwaysLastOrderingFilter]
    ordering_fields = ('name', 'modified_at', 'created_at', 'total_time', 'avg_ratings')

    # ordering = ['-avg_ratings']
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


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
