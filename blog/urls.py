from django.urls import path, re_path
from .views import PostDetailView, PostListView, PostFilterView

urlpatterns = [
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('', PostFilterView.as_view(), name='post-list'),
    # path('<slug:slug>/like', like_post, name='like-post'),
]