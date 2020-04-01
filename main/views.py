from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView, ListView, UpdateView, CreateView, DeleteView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.http import Http404
from django.db.models import Q
from main.utils import *


def base(request):
    return render(request, 'main/base.html')


def home(request):

    posts = Post.objects.all().order_by('-date_posted')
    display_type = "reg"

    context = {
        'posts': posts,
        'type': display_type
    }

    return render(request, 'main/home.html', context)


def explore(request):
    query = ""
    if request.GET:
        query = request.GET['q']

    posts = Post.objects.all().order_by('-date_posted')

    if query == "":
        if len(posts) is 0:
            messages.info(request, f'No posts to display')
        display_type = "reg"

    else:
        posts = get_query_set(posts, query)
        display_type = "search"

    top_artist, top_song, most_downloaded = get_top_stats()

    context = {
        'posts': posts,
        'type': display_type,
        'top_artist': top_artist,
        'top_song': top_song,
        'most_downloaded': most_downloaded
    }

    return render(request, 'main/explore.html', context)


def get_query_set(posts, query=None):
    queryset = []
    queries = query.split(" ")

    for q in queries:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(author__user__username__icontains=q) |
            Q(author__user__first_name__icontains=q) |
            Q(author__user__last_name__icontains=q)
        ).distinct().order_by('-date_posted')

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


class PostDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=pk)

        context = {
            'post': post
        }

        return render(request, 'main/post_detail.html', context)


class PostListViewHome(ListView):
    model = Post
    template_name = 'main/subscriptions.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'description', 'song', 'album_artwork']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author or self.request.user.is_superuser:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'song']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author or self.request.user.is_superuser:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm

    return render(request, 'main/register.html', {'form': form})


class ProfileDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == request.user.id:
            user_to_view = request.user
        elif pk is None:
            raise Http404("Could not get user.")
        else:
            user_to_view = get_object_or_404(User, id=pk, is_active=True)

        posts = Post.objects.filter(author=user_to_view.profile).order_by('-date_posted')

        is_following = False
        if self.request.user.is_authenticated and user_to_view.profile in self.request.user.is_following.all():
            is_following = True

        context = {
            'user': user_to_view,
            'posts': posts,
            'is_following': is_following
        }

        return render(request, 'main/profile.html', context)


@login_required
def update_profile(request, pk):
    if not request.user.id == pk:  # pk is the primary key of the user being edited
        messages.info(request, f'You cannot edit another user\'s account.')
        return redirect('profile', pk)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', pk)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile_update.html', context)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'main/add_comment_to_post.html', {'form': form, 'post': post})


@login_required
def delete_comment(request, pk, cpk):
    comment = get_object_or_404(Comment, comment_id=cpk)
    if comment.author == request.user.profile or request.user.is_superuser:
        comment.delete()
    return redirect('post-detail', pk=pk)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect('profile', profile_.user.id)
