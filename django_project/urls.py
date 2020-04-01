"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('main/', include('main.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from main import views as main_views
from main import ajax
from main.views import (
    ProfileDetailView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    ProfileFollowToggle,
    PostUpdateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', main_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update', main_views.update_profile, name="update-profile"),
    path('post/new/', login_required(PostCreateView.as_view()), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),
    path('post/<int:pk>/comment/', main_views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/comment/delete/<int:cpk>', main_views.delete_comment, name='delete-comment'),
    path('profile/<int:pk>/profile-follow/', login_required(ProfileFollowToggle.as_view()), name='follow'),
    # path('subscriptions/', main_views.home, name='subscriptions'),
    path('increment-song-plays/', ajax.increment_song_plays, name='increment-song-plays'),
    path('increment-song-downloads/', ajax.increment_song_downloads, name='increment-song-downloads'),
    path('increment-profile-plays/', ajax.increment_profile_plays, name='increment-profile-plays'),
    path('home/', main_views.home, name='home'),
    path('', main_views.base, name='base'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
