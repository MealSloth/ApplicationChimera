from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Post
from json import loads, dumps


def post_modify(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post_id = body.get('post_id')
        if not post_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Post.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        capacity = body.get('capacity')
        if capacity is not None:
            if type(capacity) is int:
                if capacity < post.order_count:
                    response = Result.get_result_dump(Result.POST_CAPACITY_INVALID)
                    return HttpResponse(response, content_type='application/json')
                else:
                    post.capacity = capacity
            else:
                response = Result.get_result_dump(Result.INVALID_PARAMETER)
                return HttpResponse(response, content_type='application/json')

        if body.get('name'):
            post.name = body.get('name')
        if body.get('summary'):
            post.summary = body.get('summary')

        try:
            post.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_POST)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return post

        response = {'post': model_to_dict(post)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
