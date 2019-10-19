import base
import json
import requests
from datetime import datetime
from pathlib import Path
from django.core.files import File

from movie.models import Movie, Year, Movie_Category, Qualitie, Genre, Trailer
from movie_script.movie_components.add_actors import actors
from movie_components.collection import create_collection
from movie_components.trailer import add_trailer
from movie_components.common import get_tmp_image, inside_folders, get_file
from base import conf_data


movies_path = conf_data['renamed_movie_paths']
api_key = conf_data['api_key']


def get_root_file(file_path):
    return str(file_path).split('Movies')[0]


def add_movie():
    for each_movie_path in movies_path:
        movies = Path(each_movie_path).glob("*/*/*")
        for each_movie in movies:
            split_movie = str(each_movie).split("\\")
            movie_title = split_movie[-1]
            movie_year = int(split_movie[-2])
            movie_cat = split_movie[-3]
            movie_files = inside_folders(each_movie)
            video_full_path = ""
            sub_full_path = ""

            # Go to each file and add select the latest added file
            for each_movie_file in movie_files:
                split_movie_file = str(each_movie_file).split(".")
                if split_movie_file[-1] in ('mp4', 'mkv', 'flv', 'avi', 'm4v', 'm4p'):
                    # if(split_movie_file[-1] == "mp4"):
                    if(video_full_path):
                        store_video_mtime = Path.stat(video_full_path).st_mtime
                        new_video_mtime = Path.stat(each_movie_file).st_mtime
                        if(new_video_mtime > store_video_mtime):
                            video_full_path = each_movie_file
                    else:
                        video_full_path = each_movie_file
                elif(split_movie_file[-1] == "srt"):
                    if(sub_full_path):
                        store_sub_mtime = Path.stat(sub_full_path).st_mtime
                        new_sub_mtime = Path.stat(each_movie_file).st_mtime
                        if(new_sub_mtime > store_sub_mtime):
                            sub_full_path = each_movie_file
                    else:
                        sub_full_path = each_movie_file

            video_file = get_file(video_full_path, each_movie_path)
            sub_file = get_file(
                sub_full_path, each_movie_path)
            file_size = round(Path.stat(video_full_path).st_size/1000000000, 2)
            qulity = ""

            # if the movie dont have any qulity then make it blank
            if(not video_file.find("__") == -1):
                qulity = video_file.split("__")[-2]

            # Check is this movie already added or not
            abl_movies = Movie.objects.filter(
                title=movie_title, year__year=movie_year)

            if(abl_movies):
                movie = abl_movies[0]
                if(not video_file == movie.file_path):
                    # Delete the old video file
                    old_video_file = f"{get_root_file(video_full_path)}{movie.file_path}"
                    Path(old_video_file).unlink()

                    if(movie.subtitle):
                        # Delete the old subtitle and if new update movie dont have any then set it null
                        old_sub_file = f"{get_root_file(video_full_path)}{movie.subtitle}"
                        Path(old_sub_file).unlink()
                        if(sub_file == movie.subtitle):
                            sub_file = ""

                    # Update the path
                    movie.file_path = video_file
                    movie.subtitle = sub_file
                    movie.add_date = datetime.now()
                    movie.save()

            else:
                search_movie = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_title}&page=1&include_adult=false&year={movie_year}"
                search_movie = requests.get(search_movie).json()

                if(search_movie["results"]):
                    tmdb_id = search_movie["results"][0]['id']
                    get_info = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}&language=en-US"
                    get_image = f"https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key={api_key}"
                    movie_info = requests.get(get_info).json()
                    images = requests.get(get_image).json()['backdrops']
                    genres = movie_info["genres"]
                    collection = movie_info['belongs_to_collection']

                    title = movie_info["title"]
                    tagline = movie_info['tagline']
                    overview = movie_info['overview']
                    poster = movie_info['poster_path']
                    backdrop = movie_info['backdrop_path']

                    img_1 = images[0]['file_path'] if len(images) > 0 else ''
                    img_2 = images[1]['file_path'] if len(images) > 1 else ''
                    img_3 = images[2]['file_path'] if len(images) > 2 else ''
                    img_4 = images[3]['file_path'] if len(images) > 3 else ''

                    tmdb_id = movie_info["id"]
                    imdb_id = movie_info["imdb_id"]
                    release_date = search_movie["results"][0]['release_date']

                    # Get the Year
                    year_query = Year.objects.filter(year=movie_year)
                    year = ''
                    if(not year_query):
                        year = Year(year=movie_year)
                        year.save()
                    else:
                        year = year_query[0]

                    # Get the Catagory
                    cat_query = Movie_Category.objects.filter(name=movie_cat)
                    cat = ''
                    if(not cat_query):
                        cat = Movie_Category(name=movie_cat)
                        cat.save()
                    else:
                        cat = cat_query[0]

                    # Get the Qulity
                    qut_query = Qualitie.objects.filter(title=qulity)
                    qut = ''
                    if(not qut_query):
                        qut = Qualitie(title=qulity)
                        qut.save()
                    else:
                        qut = qut_query[0]

                    # Get the Collections
                    col = create_collection(collection)

                    # # add the movie to the database
                    add_movie = Movie(title=movie_title, imdb_title=title, year=year, catagory=cat, quality=qut,
                                      tagline=tagline, overview=overview, file_path=video_file, file_size=file_size,
                                      subtitle=sub_file,  tmdb_id=tmdb_id, imdb_id=imdb_id, release_date=release_date, collections=col,)

                    if(poster):
                        img_url = f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{poster}"
                        poster_image = get_tmp_image(img_url)
                        add_movie.poster.save(
                            f"{movie_title}.jpg", File(poster_image), save=True)
                    if(backdrop):
                        backdrop_img_url = f"https://image.tmdb.org/t/p/original/{backdrop}"
                        backdrop_img = get_tmp_image(backdrop_img_url)
                        add_movie.backdrop.save(
                            f"{movie_title}_backdrop.jpg", File(backdrop_img), save=True)
                    if(img_1):
                        img_1_url = f"https://image.tmdb.org/t/p/original/{img_1}"
                        img = get_tmp_image(img_1_url)
                        add_movie.img_1.save(
                            f"{movie_title}_backdrop.jpg", File(img), save=True)
                    if(img_2):
                        img_2_url = f"https://image.tmdb.org/t/p/original/{img_2}"
                        img = get_tmp_image(img_2_url)
                        add_movie.img_2.save(
                            f"{movie_title}_backdrop.jpg", File(img), save=True)
                    if(img_3):
                        img_3_url = f"https://image.tmdb.org/t/p/original/{img_3}"
                        img = get_tmp_image(img_3_url)
                        add_movie.img_3.save(
                            f"{movie_title}_backdrop.jpg", File(img), save=True)
                    if(img_4):
                        img_4_url = f"https://image.tmdb.org/t/p/original/{img_4}"
                        img = get_tmp_image(img_4_url)
                        add_movie.img_4.save(
                            f"{movie_title}_backdrop.jpg", File(img), save=True)

                    try:
                        if(genres):
                            for genra in genres:
                                get_genres = Genre.objects.get(id=genra['id'])
                                add_movie.genres.add(get_genres)
                    except Exception as e:
                        print(e)

                    actors_list = actors(tmdb_id, add_movie)
                    add_movie.actors.set(actors_list)
                    add_trailer(tmdb_id, add_movie)

                    add_movie.save()
                    print(movie_title)


add_movie()
