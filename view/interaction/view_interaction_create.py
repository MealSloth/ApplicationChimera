from Chimera.settings import TIME_FORMAT
from Chimera.utils import model_to_dict
from Chimera.models import Interaction
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads
from datetime import datetime


def interaction_create(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        interaction_create_kwargs = {
            'user_id': body.get('user_id'),
            'assignee_id': body.get('assignee_id'),
            'interaction_type': body.get('interaction_type'),
            'message_title': body.get('message_tite'),
            'message_body': body.get('message_body'),
            'time': datetime.utcnow().strftime(TIME_FORMAT),
        }

        interaction = Interaction(**interaction_create_kwargs)

        try:
            interaction.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_INTERACTION)
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
