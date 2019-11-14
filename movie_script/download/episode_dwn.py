import os
import time
from pathlib import Path

from movie_script.base import conf_data


tv_download_path = conf_data['download_tv_path']


def episode(seasons_name, tv_year, tv_title, tv_download_link, scraping, episode_num, catagory, download):
    for season in seasons_name:
        dirname = f"{tv_download_path}/{catagory}/{tv_year}/{tv_title}/{season}/"

        # Check is that folder is available or not, if not then creat one
        if(not os.path.isdir(dirname)):
            os.makedirs(dirname)

        season_download_link = tv_download_link + season

        # Make a Soup for the episodes
        try:
            episodes_soup = scraping(
                season_download_link).find_all("td", class_="indexcolname")
        except Exception as e:
            print("This problem happend on 'tv.py' at episode function \n")
            print(e)
            episodes_soup = scraping(
                season_download_link).find_all("td", class_="indexcolname")

        # Go to each episode and take their a text
        # We ignor the 1st one because it show the prent directery
        # We use episode_num because for available episodes it start download from episode_num+1
        for i in range(episode_num+1, len(episodes_soup)):
            episode_name_split = episodes_soup[i].a.text.split(
                '.')

            # Filter the sub folder [because some tv shows have sub folder]
            if(episode_name_split[-1] == 'mp4'):
                episode_name = episodes_soup[i].a.text
                episode_file_name = episode_name.replace("Season ", "S")

                episode_download_link = f"{season_download_link}/{episode_name}"

                # Call the Downlo function that download each episode
                download(dirname, episode_file_name,
                         episode_download_link)
                # time.sleep(5)
