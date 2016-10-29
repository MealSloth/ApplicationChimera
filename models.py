from django.db.models import *
from uuid import uuid4
from enums import *


class User(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
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
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    username = CharField(max_length=254, unique=True)
    password = CharField(max_length=255)
    access_level = IntegerField(choices=UserLoginAccessLevel.UserLoginAccessLevel, default=6)

    user = ForeignKey(User)

    class Meta:
        db_table = 'user_logins'


class Location(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    purpose = IntegerField(choices=LocationPurpose.LocationPurpose, default=2)
    type = IntegerField(choices=LocationType.LocationType, default=0)
    address_line_one = CharField(max_length=255)
    address_line_two = CharField(max_length=255)
    city = CharField(max_length=255)
    state = CharField(max_length=255)
    country = CharField(max_length=255)
    zip = CharField(max_length=30)

    user = ForeignKey(User)

    class Meta:
        db_table = 'locations'


class Consumer(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    user = ForeignKey(User)
    location = ForeignKey(Location)

    class Meta:
        db_table = 'consumers'


class Chef(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    user = ForeignKey(User)
    location = ForeignKey(Location)

    class Meta:
        db_table = 'chefs'


class Album(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    time = CharField(max_length=30, editable=False)

    class Meta:
        db_table = 'albums'


class Blob(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    gcs_id = CharField(max_length=255, unique=True, editable=False)
    content_type = CharField(max_length=255, default='text/plain')
    time = CharField(max_length=30, editable=False)

    album = ForeignKey(Album)

    class Meta:
        db_table = 'blobs'


class ProfilePhoto(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    album = ForeignKey(Album)
    user = ForeignKey(User, null=True, blank=True, default=None)
    consumer = ForeignKey(Consumer, null=True, blank=True, default=None)
    chef = ForeignKey(Chef, null=True, blank=True, default=None)

    class Meta:
        db_table = 'profile_photos'


class Post(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    name = CharField(max_length=50)
    summary = CharField(max_length=255)
    order_count = IntegerField(default=0)
    capacity = IntegerField(default=1)
    post_status = IntegerField(choices=PostStatus.PostStatus, default=0)
    post_time = CharField(max_length=30)
    expire_time = CharField(max_length=30)

    chef = ForeignKey(Chef)
    location = ForeignKey(Location)
    album = ForeignKey(Album)

    class Meta:
        db_table = 'posts'


class Billing(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    user = ForeignKey(User, null=True, blank=True, default=None)
    consumer = ForeignKey(Consumer, null=True, blank=True, default=None)
    chef = ForeignKey(Chef, null=True, blank=True, default=None)
    location = ForeignKey(Location)

    class Meta:
        db_table = 'billings'


class Order(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    order_summary_id = CharField(max_length=36, default=uuid4, unique=True, editable=False)
    order_status = IntegerField(choices=OrderStatus.OrderStatus, default=0)
    order_type = IntegerField(choices=OrderType.OrderType, default=0)
    order_time = CharField(max_length=30)
    amount = IntegerField(default=1)

    post = ForeignKey(Post)
    consumer = ForeignKey(Consumer, null=True, blank=True, default=None)
    chef = ForeignKey(Chef, null=True, blank=True, default=None)
    location = ForeignKey(Location)
    billing = ForeignKey(Billing)

    class Meta:
        db_table = 'orders'


class OrderTime(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    order_status = IntegerField(choices=OrderStatus.OrderStatus, default=0)
    time = CharField(editable=False, max_length=30)

    order = ForeignKey(Order)

    class Meta:
        db_table = 'order_times'


class FavoritePost(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    consumer = ForeignKey(Consumer)
    post = ForeignKey(Post)

    class Meta:
        db_table = 'favorite_posts'


class FavoriteChef(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)

    consumer = ForeignKey(Consumer)
    chef = ForeignKey(Chef)

    class Meta:
        db_table = 'favorite_chefs'


class Review(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    rating = IntegerField()
    title = CharField(max_length=100)
    summary = CharField(max_length=1000)
    time = CharField(max_length=30, editable=False)

    post = ForeignKey(Post)
    consumer = ForeignKey(Consumer)

    class Meta:
        db_table = 'reviews'


# Siren


class Author(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)

    class Meta:
        db_table = 'authors'


class BlogPost(Model):
    id = CharField(primary_key=True, default=uuid4, max_length=36, unique=True, editable=False)
    post_time = CharField(max_length=30, editable=False)
    title = CharField(max_length=100, editable=True)
    short_description = CharField(max_length=500, editable=True)
    long_description = CharField(max_length=10000, editable=True)

    author = ForeignKey(Author)
    album = ForeignKey(Album)

    class Meta:
        db_table = "blog_posts"


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
    assignee_id = CharField(max_length=36)
    interaction_type = IntegerField(choices=InteractionType.InteractionType, default=0)
    message_title = CharField(max_length=500)
    message_body = CharField(max_length=5000)
    time = CharField(max_length=30)

    user = ForeignKey(User)

    class Meta:
        db_table = "interactions"
