import time
import requests
import shutil
from bs4 import BeautifulSoup

from base import conf_data
from download.movie_dwn import get_movies
from download.tv_dwn import get_tv_shows

headers = conf_data["headers"]

login_url = conf_data["login_url"]

login_data = conf_data["login_data"]

home_page = conf_data["home_url"]
tv_show_page = conf_data["tv_show_url"]


with requests.Session() as s:

    #########################
    # This Command Login to Mojaloss Account
    login = s.post(login_url, data=login_data, headers=headers)
    ##########################

    # This Funvction use for scriping the web
    def scraping(url):
        response = s.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    # This function use for downoad the file
    def download_file(dirname, filename, url):
        name = dirname+filename
        try:
            print(f"Now Downloading: {filename}\n")
            # with s.get(url, stream=True) as file:
            #     with open(name, 'wb') as f:
            #         shutil.copyfileobj(file.raw, f)
        except Exception as e:
            print(e)
            # # if any Error happed then this function try again to download the file
            # print(f"Now Downloading: {filename}\n Again")
            # with s.get(url, stream=True) as file:
            #     with open(name, 'wb') as f:
            #         shutil.copyfileobj(file.raw, f)

    # Here all the Tv Shows HTML links
    bangla_tv_shows = []
    english_tv_shows = []
    hindi_tv_shows = []

    # Those are for movies links
    hindi_movies = []
    english_movies = []
    tamil_movies = []
    bangla_movies = []
    koreans = []

    # Get latest Movies
    try:
        home_page_soup = scraping(home_page)

        all_post_on_home = home_page_soup.find_all(
            "div", class_='post_content_light')

        for each_movie in all_post_on_home:

            catagory_name = each_movie.find(
                "span", class_='post_category').text

            if(catagory_name == "Hindi Movies"):
                hindi_movie = each_movie.find('h2', class_="post_subtitle")
                hindi_movies.append(hindi_movie)

            elif(catagory_name == "English Movies"):
                english_movie = each_movie.find('h2', class_="post_subtitle")
                english_movies.append(english_movie)

            elif(catagory_name == "Tamil Movies"):
                tamil_movie = each_movie.find('h2', class_="post_subtitle")
                tamil_movies.append(tamil_movie)

            elif(catagory_name == "Bengali Movies"):
                bangla_movie = each_movie.find('h2', class_="post_subtitle")
                bangla_movies.append(bangla_movie)

            elif(catagory_name == "Korean"):
                korean = each_movie.find('h2', class_="post_subtitle")
                koreans.append(korean)

    except:
        print("Problem on scriping the home page main.py")

    if(len(english_movies)):
        get_movies(english_movies, scraping, "English", download_file)
    # if(len(hindi_movies)):
    #     get_movies(hindi_movies, scraping, "Hindi", download_file)

    # For getting the Tv Shows
    try:
        tv_shows_soup = scraping(tv_show_page)
        all_tv_shows = tv_shows_soup.find_all(
            "div", class_='post_content_light')

        for each_tv_show in all_tv_shows:
            catagory_name = each_tv_show.find(
                "span", class_='post_category').text

            if(catagory_name == "Bangla"):
                bangla_tv_show = each_tv_show.find(
                    'h2', class_="post_subtitle")
                bangla_tv_shows.append(bangla_tv_show)
            elif(catagory_name == "English"):
                english_tv_show = each_tv_show.find(
                    'h2', class_="post_subtitle")
                english_tv_shows.append(english_tv_show)
            elif(catagory_name == "Hindi"):
                hindi_tv_show = each_tv_show.find('h2', class_="post_subtitle")
                hindi_tv_shows.append(hindi_tv_show)
    except:
        print("Problem on scriping the tv show page main.py")

    # print(english_tv_shows)
    if(len(english_tv_shows)):
        get_tv_shows(english_tv_shows, scraping,
                     download_file, "English", login)
