
import base
from movie.models import Genre
from requests import get
import json


genres = Genre.objects.all()


def add_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=c5f91272e8db79e3deb27701f18d2894&language=en-US"
    genres = get(url).json()['genres']
    for genre in genres:
        genra_data = Genre(id=genre['id'], name=genre['name'])
        genra_data.save()


add_genres()
