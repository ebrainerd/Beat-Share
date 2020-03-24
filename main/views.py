from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import View, DetailView, ListView, UpdateView, CreateView, DeleteView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm #UserUpdateForm, ProfileUpdateForm


# class ProfileDetailView(DetailView):
#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk')
#         user_to_view = get_object_or_404(User, id=pk, is_active=True)
#
#         posts = Post.objects.filter(author=user_to_view.profile).order_by('-date_posted')
#
#         context = {
#             'posts': posts,
#             'user': user_to_view
#         }
#
#         return render(request, 'main/profile.html', context)


posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'main/home.html', context)


# class PostListViewHome(ListView):
#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#
#         if not user.is_authenticated:
#             message = "You are not logged in. Displaying all posts by default. " \
#                       + "Please sign in or register to search, view user profiles, and comments."
#             messages.info(self.request, message)
#             return render(request, 'main/home.html', {})
#
#         elif user.is_superuser:
#             qs = Post.objects.all().order_by('-date_posted')
#             message = "Logged in as administrator, " \
#                       + "currently displaying all posts."
#             messages.info(self.request, message)
#             return render(request, 'main/home.html', {'posts': qs})
#
#         else:
#             is_following_user_ids = [x.user.id for x in user.is_following.all()]
#             qs = Post.objects.filter(author__user__id__in=is_following_user_ids).order_by('-date_posted')
#             if len(qs) == 0:
#                 messages.info(self.request, "There are no posts available to show. Follow other users or wait "
#                               + "until one of the users you follow makes a post.")
#             return render(request, 'main/home.html', {'posts': qs, 'user': user})


# class PostDetailView(DetailView):
#     model = Post
#
#
# class PostCreateView(CreateView):
#     model = Post
#     fields = ['title', 'content', 'distance', 'time', 'location']
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user.profile
#         return super().form_valid(form)
#
#
# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title', 'content', 'distance', 'time', 'location']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user.profile
#         return super().form_valid(form)
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user.profile == post.author or self.request.user.is_superuser:
#             return True
#         return False
#
#
# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     success_url = '/'
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user.profile == post.author or self.request.user.is_superuser:
#             return True
#         return False


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


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile.html', context)


# @login_required
# def update_profile(request, pk):
#     if not request.user.id == pk:  # pk is the primary key of the user being edited
#         messages.info(request, f'You cannot edit another user\'s account.')
#         return redirect('user-profile', pk)
#
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('user-profile', pk)
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#
#     return render(request, 'main/profile_update.html', context)


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user.profile
#             comment.save()
#             return redirect('post-detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'main/add_comment_to_post.html', {'form': form, 'post': post})


# class ProfileFollowToggle(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         username_to_toggle = request.POST.get("username")
#         profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
#
#         return redirect('user-profile', profile_.user.id)
