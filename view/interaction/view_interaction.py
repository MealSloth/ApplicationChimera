from Chimera.utils import model_to_dict
from Chimera.models import Interaction
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads


def interaction(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        interaction_id = body.get('interaction_id')

        if not interaction_id:
            interaction_list = Interaction.objects.all()
            if interaction_list.count() > 0:
                interactions = []
                for item in interaction_list:
                    interactions.append(model_to_dict(item))
                response = {'interactions': interactions}
                Result.append_result(response, Result.SUCCESS)
                response = dumps(response)
                return HttpResponse(response, content_type='application/json')
            else:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
        else:
            try:
                current_interaction = Interaction.objects.get(pk=interaction_id)
            except Interaction.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            except Interaction.MultipleObjectsReturned:
                response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
                return HttpResponse(response, content_type='application/json')

            if kwargs:
                return current_interaction

            response = {'interaction': model_to_dict(current_interaction)}
            Result.append_result(response, Result.SUCCESS)
            response = dumps(response)
            return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
