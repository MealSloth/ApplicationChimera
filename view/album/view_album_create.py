from Chimera.utils import model_to_dict
from Chimera.settings import URL_HYDRA
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Album
from json import loads, dumps
import urllib2


def album_create(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        data = {'Hello': 'Hallo'}  # Junk args to pass null check
        re = urllib2.urlopen(URL_HYDRA + 'album/create/', data).read()

        try:
            album = Album.objects.get(pk=re.get('id'))
        except Album.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Album.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return album

        response = {'album': model_to_dict(album)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
