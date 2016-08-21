from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import User
from json import dumps, loads


def user_modify(request, **kwargs):  # /user/modify
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        user_id = body.get('user_id')
        if not user_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except User.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        if body.get('first_name'):
            user.first_name = body.get('first_name')
        if body.get('last_name'):
            user.last_name = body.get('last_name')
        if body.get('phone_number'):
            user.phone_number = body.get('phone_number')
        if body.get('gender'):
            user.gender = body.get('gender')
        if body.get('date_of_birth'):
            user.date_of_birth = body.get('date_of_birth')

        try:
            user.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_USER)
            return HttpResponse(response, content_type='application/json')

        response = {'user': model_to_dict(user)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
