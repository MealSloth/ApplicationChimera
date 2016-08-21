from Chimera.utils import model_to_dict
from Chimera.models import UserLogin
from django.http import HttpResponse
from Chimera.results import Result
from json import loads, dumps


def user_login_password_change(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        user_login_id = body.get('user_login_id')
        password = body.get('password')

        if not user_login_id and password:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            user_login = UserLogin.objects.get(pk=user_login_id)
        except UserLogin.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except UserLogin.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        user_login.password = password

        try:
            user_login.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_USER_LOGIN_PASSWORD)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return user_login

        response = {'user_login': model_to_dict(user_login)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
