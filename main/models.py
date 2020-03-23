from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileManager(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False, default="")
    followers = models.ManyToManyField(User, symmetrical=False, related_name='is_following',
                                       blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.followers.add(instance)
        instance.profile.save()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500, blank=False)
    description = models.TextField(blank=True, default="")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.FileField(blank=False, default=None)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.author.first_name)