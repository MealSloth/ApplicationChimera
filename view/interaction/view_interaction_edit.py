from Chimera.utils import model_to_dict
from Chimera.models import Interaction
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads


def interaction_edit(request, **kwargs):
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

        if body.get('user_id'):
            interaction.user_id = body.get('user_id')
        if body.get('assignee_id'):
            interaction.assignee_id = body.get('assignee_id')
        if body.get('interaction_type') and body.get('interaction_type') is not None:
            interaction.interaction_type = body.get('interaction_type')
        if body.get('message_title'):
            interaction.message_title = body.get('message_title')
        if body.get('message_body'):
            interaction.message_body = body.get('message_body')

        try:
            interaction.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_INTERACTION)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return interaction

        response = {'interaction': model_to_dict(interaction)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
