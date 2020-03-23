from django.urls import path
from .views import (
    PostListViewHome,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ProfileDetailView,
    ProfileFollowToggle,
)

urlpatterns = [
    path('', PostListViewHome.as_view(), name="main-home"),
]
