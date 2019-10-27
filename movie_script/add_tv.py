from pathlib import Path
from requests import get
from base import conf_data
from django.core.files import File

from tv.models import TV, Season, Episode, Catagory
from common import get_tmp_image, inside_folders

tv_paths = conf_data["renamed_tv_paths"]
api_key = conf_data['api_key']


def add_tv():
    for each_tv_path in tv_paths:
        tv_shows = Path(each_tv_path).glob("*/*/*")
        for each_tv_show in tv_shows:
            each_tv_show_str = str(each_tv_show).replace('\\', '/')
            split_tv_show = each_tv_show_str.split("/")
            tv_title = split_tv_show[-1].split("(")[0].strip()

            tv_year = split_tv_show[-2]
            tv_cat = split_tv_show[-3]
            tv_path = "/".join(split_tv_show[-5:])
            abl_tv_show = TV.objects.filter(title=tv_title, year=tv_year)

            if(abl_tv_show):
                seasons = inside_folders(each_tv_show)
                for each_season in seasons:
                    abl_seasons = Season.objects.filter(tv=abl_tv_show[0].id)
                    if(abl_seasons):
                        episodes = inside_folders(each_season)
                        abl_episodes = Episode.objects.filter(
                            season=abl_seasons[0].id)
                        # print(len(abl_episodes))
                        # print(len(episodes))
                        if(len(episodes) > len(abl_episodes)):
                            add_episoded_list = episodes[len(abl_episodes):]
                            print(add_episoded_list)
                            add_episodes(add_episoded_list, abl_seasons[0])
                    else:
                        season = add_season(abl_tv_show, each_season)
                        episodes = inside_folders(each_season)
                        add_episodes(episodes, season)

            else:
                # We add the tv into [array] because in add season we select the 1st item of the array
                # because we also use the filter data to season

                tv = [add_new_tv(title=tv_title, year=tv_year,
                                 catagory=tv_cat, tv_path=tv_path)]
                if(tv):
                    # Get the list of seasons
                    seasons = inside_folders(each_tv_show)
                    for each_season in seasons:
                        season = add_season(tv, each_season)
                        episodes = inside_folders(each_season)
                        add_episodes(episodes, season)


def add_season(tv_show, tv_path):
    split_season = str(tv_path).split("\\")
    season_name = split_season[-1]
    tv_season_name = f"{tv_show[0].title} {season_name}"
    season = Season(
        tv=tv_show[0], name=season_name, tv_season_name=tv_season_name)
    season.save()
    return season


def add_episodes(episodes, season):
    for each_episode in episodes:
        episode_file_name = str(
            each_episode).split("\\")[-1]
        episode_name = episode_file_name.split(".")[0]
        episode = Episode(season=season, name=episode_name,
                          file_path=episode_file_name)
        episode.save()


def add_new_tv(**tv_show):
    tv_search = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&query={tv_show['title']}&page=1"
    tv_search_result = get(tv_search).json()['results']
    if (tv_search_result):
        tv_info = tv_search_result[0]
        # print(tv_info)
        poster = tv_info['poster_path']
        backdrop = tv_info['backdrop_path']

        # Get the Catagory
        cat_query = Catagory.objects.filter(name=tv_show['catagory'])
        cat = ''
        if(not cat_query):
            cat = Catagory(name=tv_show['catagory'])
            cat.save()
        else:
            cat = cat_query[0]

        tv = TV(title=tv_show['title'], year=tv_show['year'], tmdb_title=tv_info['original_name'], overview=tv_info['overview'],
                tmdb_id=tv_info['id'], vote_average=tv_info['vote_average'], vote_count=tv_info['vote_count'], catagory=cat, tv_path=tv_show['tv_path'])

        if(poster):
            img_url = f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{poster}"
            poster_image = get_tmp_image(img_url)
            tv.poster.save(
                f"{tv_show['title']}.jpg", File(poster_image), save=True)

        if(backdrop):
            backdrop_img_url = f"https://image.tmdb.org/t/p/original/{backdrop}"
            backdrop_img = get_tmp_image(backdrop_img_url)
            tv.backdrop.save(
                f"{tv_show['title']}_backdrop.jpg", File(backdrop_img), save=True)

        tv.save()
        return tv


add_tv()
