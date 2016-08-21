from view.album import view_album_create, view_album_delete
from view.blob import view_blob_bucket_url, view_blob_delete, view_blob_upload, view_blob
from view.blog_post import view_blog_post_create, view_blog_post_delete, view_blog_post_edit
from view.consumer import view_consumer
from view.interaction import view_interaction, view_interaction_create, view_interaction_delete, view_interaction_edit
from view.order import view_order, view_order_create, view_order_delete, view_order_status_update
from view.order_time import view_order_time_create, view_order_time
from view.post import view_post, view_post_create, view_post_delete, view_post_modify, view_post_page
from view.review import view_review, view_review_create, view_review_delete, view_review_edit
from view.user import view_user, view_user_create, view_user_delete, view_user_modify
from view.user_login import view_user_login, view_user_login_password_change
from django.http import HttpResponse
from json import dumps
import jobs


# home

# /
def home(request):  # /
    response = dumps({
        'message': 'This is the MealSloth API. If you would like to learn more about MealSloth, please visit the URL.',
        'url': 'mealsloth.com',
    })
    return HttpResponse(response, content_type='application/json')


# album

# /album/create/
def album_create(request):
    return view_album_create.album_create(request)


# /album/delete/
def album_delete(request):
    return view_album_delete.album_delete(request)


# blob

# /blob/bucket/url/
def blob_bucket_url(request):
    return view_blob_bucket_url.blob_bucket_url(request)


# /blob/upload/
def blob_upload(request):
    return view_blob_upload.blob_upload(request)


# /blob/delete/
def blob_delete(request):
    return view_blob_delete.blob_delete(request)


# blob/view/
def blob(request):
    return view_blob.blob(request)


# blog-post

# /blog-post/create/
def blog_post_create(request):
    return view_blog_post_create.blog_post_create(request)


# /blog-post/delete/
def blog_post_delete(request):
    return view_blog_post_delete.blog_post_delete(request)


# /blog-post/edit/
def blog_post_edit(request):
    return view_blog_post_edit.blog_post_edit(request)


# consumer

# /consumer/
def consumer(request):
    return view_consumer.consumer(request)

# interaction

# /interaction/create/
def interaction_create(request):
    return view_interaction_create.interaction_create(request)


# /interaction/delete/
def interaction_delete(request):
    return view_interaction_delete.interaction_delete(request)


# /interaction/edit/
def interaction_edit(request):
    return view_interaction_edit.interaction_edit(request)


# /interaction/
def interaction(request):
    return view_interaction.interaction(request)


# order

# /order/
def order(request):
    return view_order.order(request)


# /order/create/
def order_create(request):
    return view_order_create.order_create(request)


# /order/delete/
def order_delete(request):
    return view_order_delete.order_delete(request)


# /order/status/update/
def order_status_update(request):
    return view_order_status_update.order_status_update(request)


# order-time

# /order-time/
def order_time(request):
    return view_order_time.order_time(request)


# /order-time/create/
def order_time_create(request):
    return view_order_time_create.order_time_create(request)


# post

# /post/
def post(request):
    return view_post.post(request)


# /post/create/
def post_create(request):
    return view_post_create.post_create(request)


# /post/delete/
def post_delete(request):
    return view_post_delete.post_delete(request)


# /post/modify/
def post_modify(request):
    return view_post_modify.post_modify(request)


# /post/page/
def post_page(request):
    return view_post_page.post_page(request)


# review

# /review/
def review(request):
    return view_review.review(request)


# /review/create/
def review_create(request):
    return view_review_create.review_create(request)


# /review/delete/
def review_delete(request):
    return view_review_delete.review_delete(request)


# /review/edit/
def review_edit(request):
    return view_review_edit.review_edit(request)


# user

# /user/
def user(request):
    return view_user.user(request)


# /user/create/
def user_create(request):
    return view_user_create.user_create(request)


# /user/delete/
def user_delete(request):
    return view_user_delete.user_delete(request)


# /user/modify/
def user_modify(request):
    return view_user_modify.user_modify(request)


# user-login

# /user-login/
def user_login(request):
    return view_user_login.user_login(request)


# /user-login/password/change/
def user_login_password_change(request):
    return view_user_login_password_change.user_login_password_change(request)


"""Jobs not included in API"""


# job

# /job/post/status/
def job_post_status(request):
    return jobs.job_post_status()


# /job/post/order/count/
def job_post_order_count(request):
    return jobs.job_post_order_count()


# /job/order/status/
def job_order_status(request):
    return jobs.job_order_status()
