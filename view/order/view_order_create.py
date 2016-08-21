from Chimera.view.order_time.view_order_time_create import order_time_create as create_order_time
from Chimera.models import Order, Consumer, User, Post
from Chimera.settings import TIME_FORMAT
from Chimera.utils import model_to_dict
from Chimera.enums import PostStatus
from django.http import HttpResponse
from Chimera.results import Result
from datetime import datetime
from json import loads, dumps


def order_create(request, **kwargs):  # /order/create
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post_id = body.get('post_id')
        consumer_id = body.get('consumer_id')
        if not (post_id and consumer_id):
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        try:
            post = Post.objects.get(pk=post_id)
            consumer = Consumer.objects.get(pk=consumer_id)
            user = User.objects.get(pk=consumer.user_id)
        except (Post.DoesNotExist, Consumer.DoesNotExist, User.DoesNotExist):
            response = Result.get_result_dump(Result.DATABASE_ENTRY_NOT_FOUND)
            return HttpResponse(response, content_type='application/json')
        except (Post.MultipleObjectsReturned, Consumer.MultipleObjectsReturned, User.MultipleObjectsReturned):
            response = Result.get_result_dump(Result.DATABASE_MULTIPLE_ENTRIES)
            return HttpResponse(response, content_type='application/json')

        if post.post_status == PostStatus.INACTIVE:
            response = Result.get_result_dump(Result.POST_INACTIVE)
            return HttpResponse(response, content_type='application/json')

        if post.post_status == PostStatus.SATURATED:
            response = Result.get_result_dump(Result.POST_SATURATED)
            return HttpResponse(response, content_type='application/json')

        if body.get('amount') + post.order_count > post.capacity:
            response = Result.get_result_dump(Result.ORDER_AMOUNT_EXCEEDS_POST_CAPACITY)
            return HttpResponse(response, content_type='application/json')

        post.order_count += body.get('amount')
        if post.order_count >= post.capacity:
            post.post_status = PostStatus.SATURATED

        order_kwargs = {
            'post_id': post.id,
            'consumer_id': consumer.id,
            'chef_id': post.chef_id,
            'location_id': consumer.location_id,
            'billing_id': user.billing_id,
            'order_type': body.get('order_type'),
            'order_time': datetime.utcnow().strftime(TIME_FORMAT),
            'amount': body.get('amount'),
        }

        order = Order(**order_kwargs)

        try:
            order.save()
            post.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_ORDER)
            return HttpResponse(response, content_type='application/json')

        order_time_kwargs = {'order_id': order.id, }

        order_time = create_order_time(request=None, **order_time_kwargs)

        if kwargs:
            return order

        response = {'order': model_to_dict(order)}  # TODO: Send 'times' dictionary
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
