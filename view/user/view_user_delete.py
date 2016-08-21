from Chimera.models import User, UserLogin, Location, Consumer, Chef, Billing, ProfilePhoto, Album
from Chimera.view.album.view_album_delete import album_delete
from django.http import HttpResponse
from Chimera.results import Result
from json import loads


def user_delete(request, **kwargs):
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

        user = User.objects.filter(pk=user_id)

        if user.count() > 0:
            user = user[0]
        else:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')

        try:
            user_login = UserLogin.objects.get(pk=user.user_login_id)
        except UserLogin.DoesNotExist:
            user_login = None

        try:
            location = Location.objects.get(pk=user.location_id)
        except Location.DoesNotExist:
            location = None

        try:
            consumer = Consumer.objects.get(pk=user.consumer_id)
        except Consumer.DoesNotExist:
            consumer = None

        try:
            chef = Chef.objects.get(pk=user.chef_id)
        except Chef.DoesNotExist:
            chef = None

        try:
            billing = Billing.objects.get(pk=user.billing_id)
        except Billing.DoesNotExist:
            billing = None

        try:
            profile_photo = ProfilePhoto.objects.get(pk=user.profile_photo_id)
        except ProfilePhoto.DoesNotExist:
            profile_photo = None

        if profile_photo:
            try:
                album = Album.objects.get(pk=profile_photo.album_id)
            except Album.DoesNotExist:
                album = None
        else:
            album = None

        if profile_photo:
            profile_photo.delete()

        if album:
            album_delete_kwargs = {'album_id': album.id}
            album_delete(request=None, **album_delete_kwargs)

        if billing:
            billing.delete()

        if consumer:
            consumer.delete()

        if chef:
            chef.delete()

        if location:
            location.delete()

        if user_login:
            user_login.delete()

        if user:
            user.delete()

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
