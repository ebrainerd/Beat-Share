from django.urls import path
from . import views
# from .views import (
#     PostListViewHome,
#     PostDetailView,
#     PostCreateView,
#     PostUpdateView,
#     PostDeleteView,
#     ProfileDetailView,
#     ProfileFollowToggle,
# )

urlpatterns = [
    path('', views.home, name='main-home'),
    # path('', PostListViewHome.as_view(), name="main-home"),
    path('register/', views.register, name="register"),
]
