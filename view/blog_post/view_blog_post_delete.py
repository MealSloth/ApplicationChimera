from Chimera.view.album.view_album_delete import album_delete as delete_album
from Chimera.models import BlogPost
from django.http import HttpResponse
from Chimera.results import Result
from json import loads


def blog_post_delete(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        blog_post_id = body.get('blog_post_id')

        if not blog_post_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            blog_post = BlogPost.objects.get(pk=blog_post_id)
        except BlogPost.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except BlogPost.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        album_delete_kwargs = {'album_id': blog_post.album_id}

        delete_album(request=None, **album_delete_kwargs)

        try:
            blog_post.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_BLOG_POST)
            return HttpResponse(response, content_type='application/json')

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
