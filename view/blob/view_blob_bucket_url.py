from Chimera.settings import URL_HYDRA
from django.http import HttpResponse
from Chimera.results import Result
import urllib2


def blob_bucket_url(request):  # /blob/bucket/url
    if request.method == 'POST':
        return HttpResponse(
            urllib2.urlopen(URL_HYDRA + 'bucket/url/'),
            content_type='application/json'
        )
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
