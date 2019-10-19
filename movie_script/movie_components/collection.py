from movie.models import Collection
from .common import get_tmp_image


def create_collection(collection):
    col = ''
    if(collection):
        collection_info = Collection.objects.filter(
            tmdb_id=collection['id'])
        if(not collection_info):
            col = Collection(
                tmdb_id=collection['id'], name=collection['name'])
            col_poster_url = f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{collection['poster_path']}"
            col_poster = get_tmp_image(col_poster_url)
            col_backdrop_url = f"https://image.tmdb.org/t/p/original{collection['backdrop_path']}"
            col_backdrop = get_tmp_image(col_backdrop_url)
            col.poster.save(f"{collection['name']}.jpg", File(
                col_poster), save=True)
            col.backdrop.save(f"{collection['name']}_backdrop.jpg", File(
                col_backdrop), save=True)
            col.save()

        else:
            col = collection_info[0]
        return col
