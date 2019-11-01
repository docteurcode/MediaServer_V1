from tv.models import Season

def add_season(tv_show, tv_path):
    split_season = str(tv_path).split("\\")
    season_name = split_season[-1]
    tv_season_name = f"{tv_show[0].title} {season_name}"
    season = Season(
        tv=tv_show[0], name=season_name, tv_season_name=tv_season_name)
    season.save()
    return season