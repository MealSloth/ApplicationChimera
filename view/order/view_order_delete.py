from Chimera.models import Order, Post
from Chimera.enums import PostStatus
from django.http import HttpResponse
from Chimera.results import Result
from json import loads


def order_delete(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
        order_id = body.get('order_id')

        if not order_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        order = Order.objects.filter(pk=order_id)
        if order.count() > 0:
            order = order[0]
        else:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')

        try:
            post = Post.objects.get(pk=order.post_id)
        except Post.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Post.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        order_amount = order.amount

        try:
            order.delete()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_DELETE_ORDER)
            return HttpResponse(response, content_type='application/json')

        post.order_count -= order_amount
        if post.post_status == PostStatus.SATURATED:
            post.post_status = PostStatus.ACTIVE

        try:
            post.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_POST)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return post

        response = Result.get_result_dump(Result.SUCCESS)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')