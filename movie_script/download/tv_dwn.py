from requests import get
import os
import time
import json
from pathlib import Path

from tv.models import TV, Season, Episode

from movie_script.download.episode_dwn import episode

from movie_script.base import conf_data

api_key = conf_data["api_key"]
tv_download_path = conf_data["download_tv_path"]


def get_tv_shows(tv_shows_url, scraping, download, catagory, login):

    for tv_show_url in tv_shows_url:
        tv_title_with_year = str(tv_show_url.a.text).replace(
            "-", "").replace("–", "").split('(')

        tv_title = tv_title_with_year[0].strip()
        tv_full_year = tv_title_with_year[-1].replace(')', '').strip()
        tv_year = tv_full_year[:4]
        tv_url = tv_show_url.a['href']
        tv_download_link = scraping(tv_url).find(
            'a', class_='alert')['href']

        if(tv_download_link):

            tv_search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&query={tv_title}&page=1&first_air_date_year={tv_year}"
            tv_responce = get(tv_search_url).json()

            if(tv_responce["results"]):
                tmdb_title = tv_responce["results"][0]['name']

                # This is just login to the mojaloss again
                login

                # Get all the seasons link here
                seasons_soup = scraping(tv_download_link).find_all(
                    "td", class_="indexcolname")
                seasons_name = []

                # Removie the 1st link because this is for back directory
                for i in range(1, len(seasons_soup)):
                    seasons_name.append(
                        seasons_soup[i].a.text.replace("/", ""))

                try:
                    tv = TV.objects.filter(title=tmdb_title, year=tv_year)

                    # if the movie abailable in the database
                    if(tv):

                        seasons = Season.objects.filter(tv=tv[0])

                        if(len(seasons_name) == len(seasons)):

                            episodes = Episode.objects.filter(
                                season=seasons[len(seasons) - 1])
                            print(episodes)
                            episode_down_from = len(episodes)

                            download_season = seasons_name[len(seasons) - 1]

                            # Download the episodes that not given
                            episode(download_season, tv_year, tv_title,
                                    tv_download_link, scraping, episode_down_from, catagory, download)

                        elif (len(seasons_name) - len(seasons) >= 1):
                            # Here we take all the season those are not added and half added
                            not_add_season = seasons_name[len(seasons) - 2:]

                            # This one is repeted Fix it
                            episodes = Episode.objects.fitler(
                                season=seasons[-1])
                            episode_down_from = len(episodes)

                            # We Convert it to the array because episode take array of seasons
                            download_season = [not_add_season[0]]

                            # We use this episode for dowbload those episode of the seasons that are not added
                            episode(download_season, tv_year, tv_title,
                                    tv_download_link, scraping, episode_down_from, catagory, download)

                            # Here we download episode of those seasons that are not added to the database
                            episode(not_add_season[1:], tv_year, tv_title,
                                    tv_download_link, scraping, 0, catagory, download)

                    else:
                        # if tv show not available in database then we download all the files
                        episode(seasons_name, tv_year, tv_title,
                                tv_download_link, scraping, 0, catagory, download)

                except Exception as e:
                    print(f"Error for: {tv_title}")
                    print(e)
