from Chimera.settings import TIME_FORMAT
from datetime import datetime, timedelta
from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Post
from json import loads, dumps


def post_page(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        page_size = body.get('page_size')
        post_time_stamp = body.get('post_time_stamp')

        if not page_size:
            page_size = 15

        if post_time_stamp:
            time = datetime.strptime(post_time_stamp, TIME_FORMAT)
        else:
            time = datetime.utcnow() + timedelta(days=99999)

        index = 0
        page_index = 0
        post_list = Post.objects.all().order_by('-post_time')
        for post_entry in post_list:
            if datetime.strptime(post_entry.post_time, TIME_FORMAT) < time:
                page_index = index
                break
            index += 1

        if post_list.count() - page_size >= page_index:
            post_list = post_list[page_index:page_index+page_size]
        elif post_list.count() - 1 >= page_index:
            post_list = post_list[page_index:]
        else:
            post_list = post_list[:page_size - 1]

        if kwargs:
            return post_list

        posts = []
        for post in post_list:
            posts.append(model_to_dict(post))

        response = {'posts': posts}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response)
