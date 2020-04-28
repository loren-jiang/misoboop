from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from django.utils import timezone

# Create your views here.
class PostListView(ListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    model = Post
    paginate_by = 10

class PostDetailView(DetailView):
    queryset = Post.objects.prefetch_related('tags')

    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
