from Chimera.settings import URL_HYDRA
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads
import urllib2


def blob_upload(request, **kwargs):  # /blob/upload
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        image_file = body.get('file')
        if not image_file:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        dictionary = {'file': image_file}
        if body.get('album_id'):
            dictionary['album_id'] = body.get('album_id')
        if body.get('url_suffix'):
            dictionary['url_suffix'] = body.get('url_suffix')
        data = dumps(dictionary)
        return HttpResponse(
            urllib2.urlopen(URL_HYDRA + 'blob/upload/', data),
            content_type='application/json'
        )
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
