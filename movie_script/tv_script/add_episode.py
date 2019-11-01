from tv.models import Episode


def add_episodes(episodes, season):
    for each_episode in episodes:
        episode_file_name = str(
            each_episode).split("\\")[-1]
        episode_name = episode_file_name.split(".")[0]
        episode = Episode(season=season, name=episode_name,
                          file_path=episode_file_name)
        episode.save()
