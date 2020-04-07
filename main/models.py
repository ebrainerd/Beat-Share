from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from PIL import Image


class ProfileManager(models.Manager):
    pass
    # def toggle_follow(self, request_profile, toggle_profile):
    #     if toggle_profile in request_profile.following.all():
    #         request_profile.following.remove(toggle_profile)
    #         toggle_profile.followers.remove(request_profile)
    #     else:
    #         request_profile.following.add(toggle_profile)
    #         toggle_profile.followers.add(request_profile)
    #     request_profile.save()
    #     toggle_profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True, default="")
    # followers = models.ManyToManyField('self', symmetrical=False, related_name="my_followers", blank=True)
    # following = models.ManyToManyField('self', symmetrical=False, blank=True)
    song_plays = models.IntegerField(blank=False, default=0)
    song_downloads = models.IntegerField(blank=False, default=0)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'

    # rescale profile pics
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProfileFollowingManager(models.Manager):
    pass


class ProfileFollowing(models.Model):
    user_prof = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    following_user_prof = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
    # When user started following
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileFollowingManager()

    class Meta:
        unique_together = ('user_prof', 'following_user_prof',)


class PostManager(models.Manager):
    pass


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500, blank=False)
    description = models.TextField(blank=True, default="")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    song = models.FileField(blank=False, default=None, upload_to='audio')
    album_artwork = models.ImageField(default='artwork-default.png', upload_to='album_covers', blank=True)
    num_plays = models.IntegerField(blank=False, default=0)
    num_downloads = models.IntegerField(blank=False, default=0)

    objects = PostManager()

    @property
    def comments(self):
        qs = Comment.objects.filter(
            Q(post__id__iexact=self.id)
        )
        return qs

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)


class CommentManager(models.Manager):
    pass


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    objects = CommentManager()

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return '{}'.format(self.content)
