from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.results import Result
from Chimera.models import Order
from json import dumps, loads


def order(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        order_id = body.get('order_id')
        post_id = body.get('post_id')
        consumer_id = body.get('consumer_id')
        chef_id = body.get('chef_id')

        if not (order_id or post_id or consumer_id or chef_id):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        current_order = None
        current_orders = None

        if order_id:
            try:
                current_order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
            except Order.MultipleObjectsReturned:
                response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
                return HttpResponse(response, content_type='application/json')
        elif post_id:
            try:
                current_orders = Order.objects.filter(post_id=post_id)
            except Order.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
        elif consumer_id:
            try:
                current_orders = Order.objects.filter(consumer_id=consumer_id)
            except Order.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
        elif chef_id:
            try:
                current_orders = Order.objects.filter(chef_id=chef_id)
            except Order.DoesNotExist:
                response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
                return HttpResponse(response, content_type='application/json')
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        if current_order is not None:
            response = {'order': model_to_dict(current_order)}
            Result.append_result(response, Result.SUCCESS)
            response = dumps(response)
            return HttpResponse(response, content_type='application/json')
        elif current_orders is not None:
            orders = []
            for order_entry in current_orders:
                orders.append(model_to_dict(order_entry))
            response = {'orders': orders}
            Result.append_result(response, Result.SUCCESS)
            response = dumps(response)
            return HttpResponse(response, content_type='application/json')
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
