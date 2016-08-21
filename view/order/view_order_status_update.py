from Chimera.view.order_time.view_order_time_create import order_time_create as create_order_time
from Chimera.settings import TIME_FORMAT
from Chimera.utils import model_to_dict
from Chimera.models import Order, Post
from Chimera.enums import OrderStatus
from django.http import HttpResponse
from Chimera.results import Result
from json import loads, dumps
from datetime import datetime


def order_status_update(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        order_id = body.get('order_id')
        order_status = body.get('order_status')

        if not (order_id and order_status):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        order_status_is_valid = False
        for entry in OrderStatus.OrderStatus:
            if entry[0] == order_status:
                order_status_is_valid = True
        if not order_status_is_valid:
            response = Result.get_result_dump(Result.ORDER_STATUS_INVALID)
            return HttpResponse(response, content_type='application/json')

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Order.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        try:
            post = Post.objects.get(pk=order.post_id)
        except Post.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Post.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        if datetime.utcnow() > datetime.strptime(post.expire_time, TIME_FORMAT):
            response = Result.get_result_dump(Result.ORDER_STATUS_POST_EXPIRED)
            return HttpResponse(response, content_type='application/json')

        order.order_status = order_status

        try:
            order.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_UPDATE_ORDER_STATUS)
            return HttpResponse(response, content_type='application/json')

        order_time_create_kwargs = {'order_id': order.id, }
        order_time = create_order_time(request=None, **order_time_create_kwargs)

        if kwargs:
            return order

        response = {'order': model_to_dict(order)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
