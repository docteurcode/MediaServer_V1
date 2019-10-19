from requests import get
from movie.models import Trailer


def add_trailer(tmdb_id, movie):
    trailer_api_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={api_key}&language=en-US"
    trailers = get(trailer_api_url).json()['results']
    if(trailers):
        for trailer in trailers:
            trailer_db = Trailer(
                movie=movie, key=trailer['key'], name=trailer['name'], site=trailer['site'], trailer_type=trailer['type'])
            trailer_db.save()
