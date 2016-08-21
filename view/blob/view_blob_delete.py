from Chimera.settings import URL_HYDRA
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads
import urllib2


def blob_delete(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        blob_id = body.get('blob_id')
        if not blob_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        else:
            data = {'blob_id': str(blob_id)}
            data = dumps(data)
            return HttpResponse(
                urllib2.urlopen(URL_HYDRA + 'blob/delete/', data),
                content_type='application/json'
            )
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
