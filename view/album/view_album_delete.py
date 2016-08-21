from Chimera.settings import URL_HYDRA
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads
import urllib2


def album_delete(request, **kwargs):  # /album/delete
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        album_id = body.get('album_id')
        if not album_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        else:
            data = {'album_id': str(album_id)}
            data = dumps(data)
            return HttpResponse(
                urllib2.urlopen(URL_HYDRA + 'album/delete/', data),
                content_type='application/json'
            )
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
