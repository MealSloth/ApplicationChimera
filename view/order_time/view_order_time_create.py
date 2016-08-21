from Chimera.models import OrderTime, Order
from Chimera.settings import TIME_FORMAT
from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from json import loads, dumps
from datetime import datetime


def order_time_create(request, **kwargs):
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

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except Order.MultipleObjectsReturned:
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        order_time = OrderTime(
            order_id=order.id,
            order_status=order.order_status,
            time=datetime.utcnow().strftime(TIME_FORMAT),
        )

        try:
            order_time.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_ORDER_TIME)
            return HttpResponse(response, content_type='application/json')

        if kwargs:
            return order_time

        response = {'order_time': model_to_dict(order_time)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')

    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
