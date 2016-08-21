from django.db.models import *
from uuid import uuid4
from enums import *


class User(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    user_login_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    consumer_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    chef_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    location_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    billing_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    profile_photo_id = CharField(default=uuid4, max_length=36, unique=True, editable=False)
    email = EmailField(max_length=254, unique=True)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    date_of_birth = CharField(max_length=30)
    gender = IntegerField(choices=Gender.Gender, default=2)
    join_date = CharField(max_length=30)

    class Meta:
        db_table = 'users'


class UserLogin(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, unique=True, editable=False)
    username = CharField(max_length=254, unique=True)
    password = CharField(max_length=255)
    access_level = IntegerField(choices=UserLoginAccessLevel.UserLoginAccessLevel, default=6)

    class Meta:
        db_table = 'user_logins'


class Post(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    chef_id = CharField(max_length=36, editable=False)
    location_id = CharField(max_length=36, editable=False)
    album_id = CharField(max_length=36, editable=False)
    name = CharField(max_length=50)
    summary = CharField(max_length=255)
    order_count = IntegerField(default=0)
    capacity = IntegerField(default=1)
    post_status = IntegerField(choices=PostStatus.PostStatus, default=0)
    post_time = CharField(max_length=30)
    expire_time = CharField(max_length=30)

    class Meta:
        db_table = 'posts'


class Order(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    post_id = CharField(max_length=36, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    chef_id = CharField(max_length=36, editable=False)
    location_id = CharField(max_length=36, editable=False)
    billing_id = CharField(max_length=36, editable=False)
    order_time_id = CharField(max_length=36, default=uuid4, unique=True, editable=False)
    order_summary_id = CharField(max_length=36, default=uuid4, unique=True, editable=False)
    order_status = IntegerField(choices=OrderStatus.OrderStatus, default=0)
    order_type = IntegerField(choices=OrderType.OrderType, default=0)
    order_time = CharField(max_length=30)
    amount = IntegerField(default=1)

    class Meta:
        db_table = 'orders'


class Location(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, editable=False)
    purpose = IntegerField(choices=LocationPurpose.LocationPurpose, default=2)
    type = IntegerField(choices=LocationType.LocationType, default=0)
    address_line_one = CharField(max_length=255)
    address_line_two = CharField(max_length=255)
    city = CharField(max_length=255)
    state = CharField(max_length=255)
    country = CharField(max_length=255)
    zip = CharField(max_length=30)

    class Meta:
        db_table = 'locations'


class Consumer(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, unique=True, editable=False)
    location_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'consumers'


class Chef(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, unique=True, editable=False)
    location_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'chefs'


class Billing(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    chef_id = CharField(max_length=36, editable=False)
    location_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'billings'


class ProfilePhoto(Model):
    id = CharField(primary_key=True, max_length=36, unique=True, editable=False)
    album_id = CharField(max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    chef_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'profile_photos'


class Album(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    time = CharField(max_length=30, editable=False)

    class Meta:
        db_table = 'albums'


class Blob(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    album_id = CharField(max_length=36, editable=False)
    gcs_id = CharField(max_length=255, unique=True, editable=False)
    content_type = CharField(max_length=255, default='text/plain')
    time = CharField(max_length=30, editable=False)

    class Meta:
        db_table = 'blobs'


class OrderTime(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    order_id = CharField(max_length=36, editable=False)
    order_status = IntegerField(choices=OrderStatus.OrderStatus, default=0)
    time = CharField(editable=False, max_length=30)

    class Meta:
        db_table = 'order_times'


class FavoritePost(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    post_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'favorite_posts'


class FavoriteChef(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    chef_id = CharField(max_length=36, editable=False)

    class Meta:
        db_table = 'favorite_chefs'


class Review(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    post_id = CharField(max_length=36, editable=False)
    consumer_id = CharField(max_length=36, editable=False)
    rating = IntegerField()
    title = CharField(max_length=100)
    summary = CharField(max_length=1000)
    time = CharField(max_length=30, editable=False)

    class Meta:
        db_table = 'reviews'


# Siren

class BlogPost(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    author_id = CharField(max_length=36, editable=False)
    album_id = CharField(default=uuid4, max_length=36,  editable=False)
    post_time = CharField(max_length=30, editable=False)
    title = CharField(max_length=100, editable=True)
    short_description = CharField(max_length=500, editable=True)
    long_description = CharField(max_length=10000, editable=True)

    class Meta:
        db_table = "blog_posts"


class Author(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)

    class Meta:
        db_table = "authors"


class Contact(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    email = EmailField(max_length=254)
    message = CharField(max_length=1000)
    time = CharField(max_length=30)

    class Meta:
        db_table = 'contact_forms'


class ContactEmail(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    email = EmailField(max_length=254)
    time = CharField(max_length=30)

    class Meta:
        db_table = "contact_emails"


# Freya

class Interaction(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    user_id = CharField(max_length=36)
    assignee_id = CharField(max_length=36)
    interaction_type = IntegerField(choices=InteractionType.InteractionType, default=0)
    message_title = CharField(max_length=500)
    message_body = CharField(max_length=5000)
    time = CharField(max_length=30)

    class Meta:
        db_table = "interactions"
