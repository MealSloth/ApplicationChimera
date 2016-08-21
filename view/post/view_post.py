from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Post
from json import dumps, loads


def post(request, **kwargs):  # /post
    if (request and request.method == 'POST') or kwargs:
        if request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post_id = body.get('post_id')
        if not post_id:
            response = Result.get_result_dump(Result.get_result_dump(Result.INVALID_PARAMETER))
            return HttpResponse(response, content_type='application/json')

        try:
            current_post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Post.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        response = {'post': model_to_dict(current_post)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
