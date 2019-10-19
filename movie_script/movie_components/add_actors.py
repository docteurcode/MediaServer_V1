from requests import get
from django.core.files import File

from movie.models import Actor, Movie_actor_name
from .common import get_tmp_image
from movie_script.base import conf_data

api_key = conf_data['api_key']


def actors(tmdb_id, movie):
    list_of_actors = []
    actor_api_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?api_key={api_key}"
    actors = get(actor_api_url).json()
    cast = ''
    if(actors['cast']):
        for actor in actors['cast']:
            try:
                get_actor = Actor.objects.filter(
                    tmdb_id=actor['id'])
                if(not get_actor):
                    cast_api = f"https://api.themoviedb.org/3/person/{actor['id']}?api_key={api_key}&language=en-US"
                    cast_info = get(
                        cast_api).json()
                    gender = 0 if cast_info['gender'] == 2 else 1
                    cast = Actor(name=actor['name'], birthday=cast_info['birthday'], gender=gender, place_of_birth=cast_info[
                        'place_of_birth'], biography=cast_info['biography'], tmdb_id=actor['id'], imdb_id=cast_info['imdb_id'])

                    cast_poster_url = f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{actor['profile_path']}"
                    cast_poster = get_tmp_image(
                        cast_poster_url)

                    cast.profile_pic.save(
                        f"{actor['name']}.jpg", File(cast_poster), save=True)
                    cast.save()
                    list_of_actors.append(cast)
                else:
                    cast = Actor.objects.get(tmdb_id=actor['id'])
                    list_of_actors.append(cast)
                # This is going to add Actor name in movie
                movie_actor = Movie_actor_name(
                    movie=movie, actor=cast, character=actor['character'], cast_num=actor['order'])
                movie_actor.save()

            except Exception as e:
                print(e)

    # print(list_of_actors)
    # movie.actors.se(list_of_actors)
    return list_of_actors
