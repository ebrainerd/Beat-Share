from django.contrib import admin
from .models import Profile, Post, ProfileFollowing, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(ProfileFollowing)
admin.site.register (Comment)
