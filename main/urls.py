from django.urls import path
from .views import PostListViewHome
from . import views

# from .views import PostListViewHome

urlpatterns = [
    # path('', PostListViewHome.as_view(), name='main-home'),
    path('', views.home, name='main-home'),
]
