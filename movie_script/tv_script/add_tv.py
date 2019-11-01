from requests import get
from django.core.files import File

from tv.models import Catagory, TV

from movie_script.base import conf_data
from movie_script.common import get_tmp_image

api_key = conf_data['api_key']


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
