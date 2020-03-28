from .models import Post, Profile
from django.http import JsonResponse

def increment_song_plays(request):
    if request.is_ajax():
        post_id = request.GET['post_id']
        post = Post.objects.get(pk=post_id)
        post.num_plays += 1
        post.save()
        return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def increment_song_downloads(request):
    if request.is_ajax():
        post_id = request.GET['post_id']
        post = Post.objects.get(pk=post_id)
        post.num_downloads += 1
        post.save()
        return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def increment_profile_plays(request):
    if request.is_ajax():
        profile_id = request.GET['profile_id']
        profile = Profile.objects.get(pk=profile_id)
        profile.song_plays += 1
        profile.save()
        return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})