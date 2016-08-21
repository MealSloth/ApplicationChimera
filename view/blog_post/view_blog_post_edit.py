from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.models import BlogPost
from Chimera.results import Result
from json import loads, dumps


def blog_post_edit(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        blog_post_id = body.get('blog_post_id')
        author_id = body.get('author_id')
        title = body.get('title')
        short_description = body.get('short_description')
        long_description = body.get('long_description')

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

        if author_id:
            blog_post.author_id = author_id
        if title:
            blog_post.title = title
        if short_description:
            blog_post.short_description = short_description
        if long_description:
            blog_post.long_description = long_description

        try:
            blog_post.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOG_POST)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return blog_post

        response = {'blog_post': model_to_dict(blog_post)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
