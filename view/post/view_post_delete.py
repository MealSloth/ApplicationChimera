from Chimera.view.album.view_album_delete import album_delete
from Chimera.view.order.view_order_delete import order_delete
from Chimera.models import Post, Order
from django.http import HttpResponse
from Chimera.results import Result
from json import loads


def post_delete(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post_id = body.get('post_id')

        if not post_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post = Post.objects.filter(pk=post_id)

        if post.count() > 0:
            post = post[0]
        else:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')

        orders_list = Order.objects.filter(post_id=post.id)
        for order in orders_list:
            order_delete_kwargs = {'order_id': order.id}
            order_delete(request=None, **order_delete_kwargs)

        album_id = post.album_id

        try:
            post.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_POST)
            return HttpResponse(response, content_type='application/json')

        album_delete_kwargs = {'album_id': album_id, }

        album_delete(request=None, **album_delete_kwargs)

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')