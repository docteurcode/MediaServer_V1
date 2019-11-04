from requests import get
import os
import time
import json
from pathlib import Path

from tv.models import TV, Season

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

        #         # each_tv_info = {'title': tv_title, 'year': tv_year,
        #         #                 'url': tv_url, 'download_link': tv_download_link, "seasons": seasons_name}

                try:
                    tv = TV.objects.filter(title=tmdb_title, year=tv_year)

                    # if the movie abailable in the database
                    if(tv):
                        print(tv[0].id)
                        seasons = Season.objects.filter(id=tv[0].id)
                        print(seasons)

                    #     # if it has any season then it work
                    #     if(len(seasons_available)):
                    #         season_id = seasons_available[-1][0]
                    #         seasons = seasons_name[len(
                    #             seasons_available) - 1:]
                    #         check_season = [seasons[0]]

                    #         episode_query = f"SELECT episode_id, episode_name FROM tv_episodes WHERE season_id={season_id}"
                    #         db.execute(episode_query)
                    #         episodes = db.fetchall()
                    #         episode_down_from = len(episodes) + 1
                    #         print(f"{episode_down_from} and {check_season}")

                    # #         # Download the episodes that not given
                    # #         episode(check_season, tv_year, tv_title,
                    # #                 tv_download_link, scraping, episode_down_from, catagory, download)

                    # #         # if the more then 1 seasons not download then
                    # #         if(len(seasons) > 1):
                    # #             full_down_seasons = seasons[1:]

                    # #             episode(full_down_seasons, tv_year,
                    # #                     tv_title, tv_download_link, scraping, 0, catagory, download)

                    # if tv show not available in database then we download all the files
                    # else:
                    #     episode(seasons_name, tv_year, tv_title,
                    #             tv_download_link, scraping, 0, catagory, download)

                except:
                    print(f"Error for: {tv_title}")
