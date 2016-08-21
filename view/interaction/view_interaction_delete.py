from Chimera.models import Interaction
from django.http import HttpResponse
from Chimera.results import Result
from json import loads


def interaction_delete(request, **kwargs):
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
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            interaction = Interaction.objects.get(pk=interaction_id)
        except Interaction.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Interaction.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        try:
            interaction.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_INTERACTION)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return True

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
