from movie.models import Qualitie


def get_or_add_quality(qulity):
    # Get the Qulity
    qut_query = Qualitie.objects.filter(title=qulity)
    qut = ''
    if(not qut_query):
        qut = Qualitie(title=qulity)
        qut.save()
    else:
        qut = qut_query[0]
    return qut
