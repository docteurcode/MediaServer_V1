import os
from pathlib import Path
from movie.models import Mojaloss

from movie_script.base import conf_data

movie_download_path = conf_data["download_movie_path"]


def get_movies(movies_url, scraping, catagory, download):
    for each_movie_url in movies_url:

        movie_full_title = str(
            each_movie_url.a.text).replace(")", "").split('(')

        movie_title = movie_full_title[0].strip().replace(":", "")
        try:

            if(len(movie_full_title) > 1):
                split_movie_year = movie_full_title[-1].split(" ")
                movie_year = split_movie_year[0].strip()

                movie_url = each_movie_url.a['href']
                movie_file = ""
                movie_sub = ""
                # if any Sub folder available then the sub store in that sub 2
                movie_sub_2 = ""

                movie_download_links = scraping(movie_url).find(
                    'a', class_='alert')['href']
                movie_soup = scraping(movie_download_links).find_all(
                    "td", class_="indexcolname")

                for each_file in range(1, len(movie_soup)):
                    file_name = movie_soup[each_file].a.text
                    file_name_split = file_name.split(".")

                    if(file_name_split[-1] == "mp4"):
                        movie_file = file_name
                    elif(file_name_split[-1] == 'srt'):
                        movie_sub = file_name

                    # If this movie have Sub folder then it goes to that folder and get the sub
                    elif(file_name == "Subs/"):
                        sub_download_links = movie_download_links + file_name
                        sub_soup = scraping(sub_download_links).find_all(
                            "td", class_="indexcolname")
                        for each_sub in range(1, len(sub_soup)):
                            sub = sub_soup[each_sub].a.text
                            sub_split = sub.split(".")
                            if(sub_split[-1] == 'srt'):
                                movie_sub_2 = f"Subs/{sub}"

                # Download the Movie file
                dirname = f"{movie_download_path}/{catagory}/{movie_year}/{movie_title}/"

                abl_movie = Mojaloss.objects.filter(
                    title=movie_title, year=movie_year)

                # This Function download the movie and subtitle
                def down_mov_sub():
                        # If the folder not created then it will be create one
                    if(not os.path.isdir(dirname)):
                        os.makedirs(dirname)

                    movie_down_url = movie_download_links + movie_file
                    download(dirname, movie_file, movie_down_url)

                    # If sub available then download the subtitle
                    if(movie_sub):
                        sub_down_url = movie_download_links + movie_sub
                        download(dirname, movie_sub, sub_down_url)
                    elif(movie_sub_2):
                        sub_title = "eng_sub.srt"
                        sub_down_url = movie_download_links + movie_sub_2
                        download(dirname, sub_title, sub_down_url)

                # # If not available then we add those to the database and download the movie
                if(not abl_movie):
                    down_mov_sub()
                    movie = Mojaloss(title=movie_title,
                                     year=movie_year, path=movie_file)
                    movie.save()

                elif(abl_movie and not abl_movie[0].path == movie_file):
                    down_mov_sub()
                    abl_movie.path = movie_file
                    abl_movie.save()

        except:
            print(f"Find Problem on {movie_title}")
