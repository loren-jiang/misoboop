from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from django.utils import timezone
from blog.filters import PostFilterSet
from django_filters.views import FilterView
from core.models import BasicTag
from django.db.models import Count, F, Q
from django.conf import settings

# Create your views here.
# class PostListView(ListView):
#     model = Post
#     paginate_by = 10

#     def get_queryset(self):
#         qs = super().get_queryset().prefetch_related('tags',)
#         return qs


class PostFilterView(FilterView):
    model = Post
    filterset_class = PostFilterSet
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('tags',)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['post_tags'] = Post.tags.most_common().filter(filterable=True
                                                              ).annotate(count=Count('id')).order_by('-num_times')[0:10]
        context['latest_posts'] = Post.objects.order_by('-created_at')[0:10]
        return context


class PostDetailView(DetailView):
    queryset = Post.objects.prefetch_related('tags')

    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['disqus_shortname'] = settings.DISQUS_WEBSITE_SHORTNAME
        return context
