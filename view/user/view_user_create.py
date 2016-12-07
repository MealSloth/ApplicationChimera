from Chimera.models import User, UserLogin, Location, Consumer, Chef, Billing, Album, ProfilePhoto
from Chimera.utils import format_phone_number, model_to_dict
from Chimera.settings import TIME_FORMAT
from django.http import HttpResponse
from Chimera.results import Result
from json import dumps, loads
from datetime import datetime


def user_create(request, **kwargs):  # /user/create
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        if not body.get('email') and body.get('password'):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        user_kwargs = {'email': body.get('email')}

        if body.get('first_name'):
            user_kwargs['first_name'] = body.get('first_name')
        if body.get('last_name'):
            user_kwargs['last_name'] = body.get('last_name')
        if body.get('phone_number'):
            user_kwargs['phone_number'] = format_phone_number(1, body.get('phone_number'))
        if body.get('gender'):
            user_kwargs['gender'] = body.get('gender')
        if body.get('date_of_birth'):
            user_kwargs['date_of_birth'] = body.get('date_of_birth')
        user_kwargs['join_date'] = datetime.utcnow().strftime(TIME_FORMAT)

        current_user = User(**user_kwargs)

        if User.objects.filter(email=current_user.email):
            response = Result.get_result_dump(Result.EMAIL_IN_USE)
            return HttpResponse(response, content_type='application/json')
        else:
            current_user.save()

        current_user_login = UserLogin(
            user=current_user,
            username=current_user.email,
            password=body.get('password'),
        )

        current_user_login.save()

        if not UserLogin.objects.filter(id=current_user_login.id):
            current_user.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        location = Location(
            user=current_user,
        )

        location.save()

        if not Location.objects.filter(id=location.id):
            current_user.delete()
            current_user_login.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        consumer = Consumer(
            user=current_user,
            location=location,
        )

        consumer.save()

        if not Consumer.objects.filter(id=consumer.id):
            current_user.delete()
            current_user_login.delete()
            location.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        chef = Chef(
            user=current_user,
            location=location,
        )

        chef.save()

        if not Chef.objects.filter(id=chef.id):
            current_user.delete()
            current_user_login.delete()
            location.delete()
            consumer.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        billing = Billing(
            user=current_user,
            consumer=consumer,
            chef=chef,
            location=location,
        )

        billing.save()

        if not Billing.objects.filter(id=billing.id):
            current_user.delete()
            current_user_login.delete()
            consumer.delete()
            chef.delete()
            location.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        album = Album(time=datetime.utcnow().strftime(TIME_FORMAT))

        album.save()

        if not Album.objects.filter(id=album.id):
            current_user.delete()
            current_user_login.delete()
            consumer.delete()
            chef.delete()
            location.delete()
            billing.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        profile_photo = ProfilePhoto(
            album=album,
            user=current_user,
        )

        profile_photo.save()

        if not ProfilePhoto.objects.filter(id=profile_photo.id):
            current_user.delete()
            current_user_login.delete()
            consumer.delete()
            chef.delete()
            location.delete()
            billing.delete()
            album.delete()
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        current_user = User.objects.get(pk=current_user.id)
        current_user_login = UserLogin.objects.get(pk=current_user_login.id)

        if not current_user and current_user_login:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE)
            return HttpResponse(response, content_type='application/json')

        current_user_json = model_to_dict(current_user)
        current_user_login_json = model_to_dict(current_user_login)

        if kwargs:
            return current_user

        response = {'user': current_user_json, 'user_login': current_user_login_json}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')