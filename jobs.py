from enums import PostStatus, OrderStatus
from datetime import timedelta, datetime
from Chimera.settings import TIME_FORMAT
from django.http import HttpResponse
from models import Post, Order
from results import Result


def job_post_status():
    post_list = Post.objects.all()
    for post in post_list:
        if datetime.utcnow() > datetime.strptime(post.expire_time, TIME_FORMAT):
            post.post_status = PostStatus.INACTIVE
            try:
                post.save()
            except StandardError, error:
                print(error)
        elif post.post_status == PostStatus.SATURATED and post.order_count < post.capacity:
            post.post_status = PostStatus.ACTIVE
            try:
                post.save()
            except StandardError, error:
                print(error)
    response = Result.get_result_dump(Result.SUCCESS)
    return HttpResponse(response, content_type='application/json')


def job_post_order_count():
    post_list = Post.objects.all()
    for post in post_list:
        order__list = Order.objects.filter(post_id=post.id)
        count = 0
        for order in order__list:
            count += order.amount
        post.order_count = count
        if post.order_count == post.capacity:
            post.post_status = PostStatus.SATURATED
        try:
            post.save()
        except StandardError, error:
            print(error)
    response = Result.get_result_dump(Result.SUCCESS)
    return HttpResponse(response, content_type='application/json')


def job_order_status():
    order_list = Order.objects.all()
    for order in order_list:
        order_time = datetime.strptime(order.order_time, TIME_FORMAT)
        if datetime.utcnow() - order_time > timedelta(days=1):
            order.order_status = OrderStatus.DELIVERED
            try:
                order.save()
            except StandardError, error:
                print(error)
    response = Result.get_result_dump(Result.SUCCESS)
    return HttpResponse(response, content_type='application/json')
