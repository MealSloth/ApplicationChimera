from django.http import HttpResponse
from Chimera.models import UserLogin
from Chimera.results import Result
from json import dumps, loads


def user_login(request):  # /user-login
    if request.method == 'POST':
        body = loads(request.body)
        user_login_id = body.get('user_login_id')
        user_id = body.get('user_id')
        if user_login_id:
            if UserLogin.objects.filter(id=user_login_id).values().count() > 0:
                current_user_login = UserLogin.objects.filter(id=user_login_id).values()[0]
                response = {'user_login': current_user_login}
                Result.append_result(response, Result.SUCCESS)
                response = dumps(response)
                return HttpResponse(response, content_type='application/json')
        elif user_id:
            if UserLogin.objects.filter(user_id=user_id).values().count() > 0:
                current_user_login = UserLogin.objects.filter(user_id=user_id).values()[0]
                response = {'user_login': current_user_login}
                Result.append_result(response, Result.SUCCESS)
                response = dumps(response)
                return HttpResponse(response, content_type='application/json')
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')