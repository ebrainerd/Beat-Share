from django.db.models import Max
from .models import Post, Profile

def get_top_stats():

    top_song = Post.objects.all().aggregate(
        topsong=Max('num_plays')
    )['topsong']
    top_song = Post.objects.filter(num_plays=top_song).first()

    top_artist = Profile.objects.all().aggregate(
        topartist=Max('song_plays')
    )['topartist']
    top_artist = Profile.objects.filter(song_plays=top_artist).first()

    top_downloaded_song = Post.objects.all().aggregate(
        topdownloadedsong=Max('num_downloads')
    )['topdownloadedsong']
    top_downloaded_song = Post.objects.filter(num_downloads=top_downloaded_song).first()

    return top_song, top_artist, top_downloaded_song
