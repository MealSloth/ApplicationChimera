from Chimera.enums import OrderStatus
from django.http import HttpResponse
from Chimera.models import OrderTime
from Chimera.results import Result
from json import loads, dumps


def order_time(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        order_time_id = body.get('order_time_id')
        order_id = body.get('order_id')

        if not order_time_id and not order_id:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        if order_time_id:
            try:
                current_order_time = OrderTime.objects.get(pk=order_time_id)
            except OrderTime.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            except OrderTime.MultipleObjectsReturned:
                response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
                return HttpResponse(response, content_type='application/json')
            if kwargs:
                return current_order_time
            else:
                response = {'order_time': current_order_time}
                Result.append_result(response, Result.SUCCESS)
                response = dumps(response)
                return HttpResponse(response, content_type='application/json')
        elif order_id:
            try:
                order_times = OrderTime.objects.filter(order_id=order_id)
            except OrderTime.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            times = {}
            for order_status_entry in OrderStatus.OrderStatus:
                times[order_status_entry[0]] = []
            for order_times_entry in order_times:
                times[order_times_entry.order_status].append(order_times_entry.time)
            if kwargs:
                return times
            else:
                response = {'times': times}
                Result.append_result(response, Result.SUCCESS)
                response = dumps(response)
                return HttpResponse(response, content_type='application/json')
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')

