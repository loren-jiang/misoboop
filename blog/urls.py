from django.urls import path, re_path
from .views import PostDetailView, PostListView

urlpatterns = [
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('', PostListView.as_view(), name='post-list'),
    # path('<slug:slug>/like', like_post, name='like-post'),
]