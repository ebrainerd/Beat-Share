from django.urls import path
from .views import PostListView
from . import views

# from .views import PostListViewHome

urlpatterns = [
    path('', PostListView.as_view(), name='main-home'),
    # path('', PostListViewHome.as_view(), name='main-home'),
]
