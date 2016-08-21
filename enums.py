class Months:
    def __init__(self):
        pass

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    Months = (
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December'),
    )


class Gender:
    def __init__(self):
        pass

    MALE = 0
    FEMALE = 1
    OTHER = 2

    Gender = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )


class UserLoginAccessLevel:
    def __init__(self):
        pass

    SUPER_ADMIN = 0
    CHEF_ADMIN = 1
    CONSUMER_ADMIN = 2
    CONSUMER_CHEF = 3
    CHEF = 4
    CONSUMER = 5
    TRIAL = 6

    UserLoginAccessLevel = (
        (SUPER_ADMIN, 'SuperAdmin'),
        (CHEF_ADMIN, 'ChefAdmin'),
        (CONSUMER_ADMIN, 'ConsumerAdmin'),
        (CONSUMER_CHEF, 'ConsumerChef'),
        (CHEF, 'Chef'),
        (CONSUMER, 'Consumer'),
        (TRIAL, 'Trial'),
    )


class PostStatus:
    def __init__(self):
        pass

    ACTIVE = 0
    SATURATED = 1
    INACTIVE = 2

    PostStatus = (
        (ACTIVE, 'Active'),
        (SATURATED, 'Saturated'),
        (INACTIVE, 'Inactive'),
    )


class OrderStatus:
    def __init__(self):
        pass

    PENDING = 0
    RECEIVED = 1
    PROGRESS = 2
    COMPLETED = 3
    SHIPPED = 4
    DELIVERED = 5
    DISPUTED = 6
    CANCELLED = 7

    OrderStatus = (
        (PENDING, 'Pending'),
        (RECEIVED, 'Received'),
        (PROGRESS, 'Progress'),
        (COMPLETED, 'Completed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (DISPUTED, 'Disputed'),
        (CANCELLED, 'Cancelled'),
    )


class OrderType:
    def __init__(self):
        pass

    PICKUP = 0
    DELIVERY = 1
    DINEIN = 2

    OrderType = (
        (PICKUP, 'Pickup'),
        (DELIVERY, 'Delivery'),
        (DINEIN, 'DineIn'),
    )


class LocationPurpose:
    def __init__(self):
        pass

    BILLING = 0
    POST = 1
    DISPLAY = 2

    LocationPurpose = (
        (BILLING, 'Billing'),
        (POST, 'Post'),
        (DISPLAY, 'Display'),
    )


class LocationType:
    def __init__(self):
        pass

    RESIDENTIAL = 0
    COMMERCIAL = 1

    LocationType = (
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
    )


class InteractionType:
    def __init__(self):
        pass

    OUTGOING_TASK = 0
    CUSTOMER_HELP_CALL = 1
    ORDER_DISPUTE = 2
    COMPLIMENT = 3
    COMPLAINT = 4

    InteractionType = (
        (OUTGOING_TASK, 'Outgoing Task'),
        (CUSTOMER_HELP_CALL, 'Customer Help Call'),
        (ORDER_DISPUTE, 'Order Dispute'),
        (COMPLIMENT, 'Compliment'),
        (COMPLAINT, 'Complaint'),
    )
