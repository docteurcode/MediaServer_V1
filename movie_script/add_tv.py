from pathlib import Path
from requests import get


from base import conf_data
from tv.models import TV, Season, Episode
from common import get_tmp_image, inside_folders
from tv_script.add_tv import add_new_tv
from tv_script.add_season import add_season
from tv_script.add_episode import add_episodes

tv_paths = conf_data["renamed_tv_paths"]


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

                        if(len(episodes) > len(abl_episodes)):
                            # Those episode path get from Database
                            episode_paths = [
                                db_episode.file_path for db_episode in abl_episodes]

                            # Go to each episode and check is that episode added or not
                            for episode in episodes:
                                episode_file = str(episode).replace(
                                    "\\", "/").split("/")[-1]
                                if episode_file not in episode_paths:
                                    add_episodes([episode], abl_seasons[0])
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


add_tv()
