from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',


    # home

    # /
    url(r'^$', views.home, name='/'),


    # album

    # /album/create/  ## INTERNAL
    url(r'^album/create/$', views.album_create, name='album/create/'),

    # /album/delete/
    url(r'^album/delete/$', views.album_delete, name='album/delete/'),


    # blob

    # /blob/bucket/
    url(r'^blob/bucket/url/$', views.blob_bucket_url, name='blob/bucket/url/'),

    # /blob/upload/
    url(r'^blob/upload/$', views.blob_upload, name='blob/upload/'),

    # /blob/delete/
    url(r'blob/delete/$', views.blob_delete, name='blob/delete/'),

    # /blob/view/
    url(r'^blob/$', views.blob, name='blob/'),


    # blog-post

    # /blog-post/create/  ## INTERNAL
    # url(r'^blog-post/create/$', views.blog_post_create, name='blog-post/create/'),

    # /blog-post/delete/  ## INTERNAL
    # url(r'^blog-post/delete/$', views.blog_post_delete, name='blog-post/delete/'),

    # /blog-post/edit/  ## INTERNAL
    # url(r'^blog-post/edit/$', views.view_blog_post_edit, name='blog-post/edit/'),


    # consumer

    # /consumer/
    url(r'^consumer/$', views.consumer, name='consumer/'),


    # interaction

    # /interaction/create/
    url(r'^interaction/create/$', views.interaction_create, name='interaction/create/'),

    # /interaction/delete/  ## INTERNAL
    # url(r'^interaction/delete/$', views.interaction_delete, name='interaction/delete/'),

    # /interaction/edit/
    url(r'^interaction/edit/$', views.interaction_edit, name='interaction/edit/'),

    # /interaction/
    url(r'^interaction/$', views.interaction, name='interaction'),


    # order

    # /order/create/
    url(r'^order/create/$', views.order_create, name='order/create/'),

    # /order/delete/  ## INTERNAL
    # url(r'^order/delete/$', views.order_delete, name='order/delete/'),

    # /order/status/update/
    url(r'^order/status/update/$', views.order_status_update, name='order/status/update/'),

    # /order/
    url(r'^order/$', views.order, name='order/'),


    # order-time

    # /order-time/
    url(r'^order-time/$', views.order_time, name='order-time/'),

    # /order-time/create/  ## INTERNAL
    # url(r'^order-time/create/$', views.order_time_create, name='order-time/create/'),


    # post

    # /post/create/
    url(r'^post/create/$', views.post_create, name='post/create/'),

    # /post/delete/  ## INTERNAL
    # url(r'^post/delete/$', views.post_delete, name='post/delete/'),

    # /post/modify/
    url(r'^post/modify/$', views.post_modify, name='post/modify/'),

    # /post/page/
    url(r'^post/page/$', views.post_page, name='post/page/'),

    # /post/
    url(r'^post/$', views.post, name='post/'),


    # review

    # /review/
    url(r'^review/$', views.review, name='review/'),

    # /review/create/
    url(r'^review/create/$', views.review_create, name='review/create/'),

    # /review/delete/
    url(r'^review/delete/$', views.review_delete, name='review/delete/'),

    # /review/edit/
    url(r'^review/edit/$', views.review_edit, name='review/edit/'),


    # user

    # /user/modify/
    url(r'^user/modify/$', views.user_modify, name='user/modify/'),

    # /user/create/
    url(r'^user/create/$', views.user_create, name='user/create/'),

    # /user/delete/  ## INTERNAL
    # url(r'^user/delete/$', views.user_delete, name='user/delete/'),

    # /user/
    url(r'^user/$', views.user, name='user/'),


    # user_login
    
    # /user-login/password/change/
    url(r'^user-login/password/change/$', views.user_login_password_change, name='user-login/password/change/'),

    # /user-login/
    url(r'^user-login/$', views.user_login, name='user-login/'),


    # job

    # /job/post/
    url(r'^job/post/status/$', views.job_post_status, name='job/post/status/'),
    url(r'^job/post/order/count/$', views.job_post_order_count, name='job/post/order/count/'),

    # /job/order/
    url(r'^job/order/status/$', views.job_order_status, name='job/order/status/'),
)
