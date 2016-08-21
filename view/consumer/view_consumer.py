from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.models import Consumer
from Chimera.results import Result
from json import dumps, loads


def consumer(request, **kwargs):  # /consumer
    if (request and request.method == 'POST') or kwargs:
        if request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        consumer_id = body.get('consumer_id')
        if not consumer_id:
            response = Result.get_result_dump(Result.get_result_dump(Result.INVALID_PARAMETER))
            return HttpResponse(response, content_type='application/json')

        try:
            current_consumer = Consumer.objects.get(pk=consumer_id)
        except Consumer.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Consumer.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        favorite_posts = []  # TODO: Add favorite posts

        favorite_chefs = []  # TODO: Add favorite chefs

        favorite_posts_json = []
        favorite_chefs_json = []
        for post in favorite_posts:
            favorite_posts_json += model_to_dict(post)
        for chef in favorite_chefs:
            favorite_chefs_json += model_to_dict(chef)

        consumer_json = model_to_dict(current_consumer)
        consumer_json['favorite_posts'] = favorite_posts_json
        consumer_json['favorite_chefs'] = favorite_chefs_json

        response = {
            'consumer': consumer_json,
        }
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
