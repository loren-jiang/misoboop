import django_filters
from .models import Post
from django.contrib.postgres.search import SearchVector
from core.filters import SearchFilter
from core.models import BasicTag
from django import forms
from django_filters import OrderingFilter

class PostFilterSet(django_filters.FilterSet):
    search = SearchFilter(lookups=['headline', 'tags__name', 'short_description'], label='Search blog posts')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=BasicTag.objects.filter(filterable=True, post__isnull=False).distinct(),
        to_field_name='name',
        field_name='tags__name',
    )
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('created_at', 'created_at'),
        ),

        # labels do not need to retain order
        field_labels={
            'created_at': 'Date',
        }
    )

    class Meta:
        model = Post
        fields = {
            # 'headline': ['icontains'],
        }
