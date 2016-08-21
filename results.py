from json import dumps


class Result:
    def __init__(self):
        pass

    """Universal results"""

    # 1000-1999
    SUCCESS = 1000  # Used generically any time the expected outcome is achieved

    # 9000-9999
    INVALID_PARAMETER = 9000  # Used any time a parameter is invalid or missing
    POST_ONLY = 9001  # Used any time a POST-only method is requested by an HTTP method other than POST (GET, PUT, etc.)
    GET_ONLY = 9002  # Generally not used, as Chimera's API is intended to be accessible only by POST
    DATABASE_CANNOT_SAVE = 9003  # Used generically when an item cannot be saved to the database
    DATABASE_ENTRY_NOT_FOUND = 9004  # Used when a request is made for a database entry which does not exist
    DATABASE_MULTIPLE_ENTRIES = 9005  # Used when one database entry is expected but the result is more than one

    """Method-specific results"""

    # 2000-2009 /user/create/
    EMAIL_IN_USE = 2000  # Used when a request provides an email address which is already registered

    # 2010-2019 /user/modify/
    DATABASE_CANNOT_UPDATE_USER = 2010  # Used when a User cannot be updated in the database

    # 2040-2049 /blob/
    HYDRA_ERROR = 2040  # Used generically when an error is received from Hydra
    DATABASE_CANNOT_SAVE_ALBUM = 2041  # Used in Hydra when an Album model cannot be saved to the database
    DATABASE_CANNOT_SAVE_BLOB = 2042  # Used in Hydra when a Blob model cannot be saved to the database
    STORAGE_CANNOT_SAVE_BLOB = 2043  # Used in Hydra when a Blob cannot be saved to storage
    FILETYPE_INVALID = 2044  # Used in Hydra when a filetype is invalid
    BLOB_COUNT_INVALID = 2045  # Used when a request for blobs provides a count which exceeds total blob count

    # 2050-2059 /blob/delete/
    STORAGE_CANNOT_DELETE_BLOB = 2050  # Used in Hydra when a Blob cannot be deleted from storage
    DATABASE_CANNOT_DELETE_BLOB = 2051  # Used in Hydra when a Blob cannot be deleted from the database
    DATABASE_CANNOT_DELETE_ALBUM = 2052  # Used in Hydra when an Album cannot be deleted from the database

    # 2060-2069 /post/create/
    DATABASE_CANNOT_SAVE_POST = 2060  # Used when a Post cannot be saved to the database

    # 2070-2079 /post/delete/
    DATABASE_CANNOT_DELETE_POST = 2070  # Used when a Post cannot be deleted from the database

    # 2080-2089 /order/delete/
    DATABASE_CANNOT_DELETE_ORDER = 2080  # Used when an Order cannot be deleted from the database

    # 2090-2099 /order/create/
    ORDER_AMOUNT_EXCEEDS_POST_CAPACITY = 2090  # Used when an Order requests more than a post's capacity
    DATABASE_CANNOT_SAVE_ORDER = 2091  # Used when an Order cannot be saved to the database
    POST_INACTIVE = 2092  # Used when an Order is requested for an inactive post
    POST_SATURATED = 2093  # Used when an Order is requested for a saturated post

    # 2100-2109 /order-time/create/
    DATABASE_CANNOT_SAVE_ORDER_TIME = 2100  # Used when an OrderTime cannot be saved to the database

    # 2110-2119 /blog-post/create/
    DATABASE_CANNOT_SAVE_BLOG_POST = 2110  # Used when a BlogPost cannot be saved to the database

    # 2120-2129 /blog-post/delete/
    DATABASE_CANNOT_DELETE_BLOG_POST = 2120  # Used when a BlogPost cannot be deleted from the database

    # 2130-2139 /post/modify/
    POST_CAPACITY_INVALID = 2130  # Used when a request for /post/modify/ uses invalid capacity
    DATABASE_CANNOT_UPDATE_POST = 2131  # Used when a Post cannot be updated in the database

    # 2140-2149 /user-login/password/change/
    DATABASE_CANNOT_UPDATE_USER_LOGIN_PASSWORD = 2140  # Used when a UserLogin password cannot be updated

    # 2150-2159 /order/status/update/
    DATABASE_CANNOT_UPDATE_ORDER_STATUS = 2150  # Used when an Order order_status cannot be updated
    ORDER_STATUS_INVALID = 2151  # Used generically when a request is made for an order status which is invalid
    ORDER_STATUS_POST_EXPIRED = 2152  # Used when a request is made to update an expired order

    # 2160-2169 /interaction/create/
    DATABASE_CANNOT_SAVE_INTERACTION = 2160  # Used when an Interaction cannot be saved to the database

    # 2170-2179 /interaction/delete/
    DATABASE_CANNOT_DELETE_INTERACTION = 2170  # Used when an Interaction cannot be deleted from the database

    # 2180-2189 /interaction/edit/
    DATABASE_CANNOT_UPDATE_INTERACTION = 2180  # Used when an Interaction cannot be updated in the database

    # 2190-2199 /review/create/
    DATABASE_CANNOT_SAVE_REVIEW = 2190  # Used when a Review cannot be saved to the database
    RATING_INVALID = 2191  # Used when a supplied rating is not a valid integer in the range 0 to 10 inclusive

    # 2200-2209 /review/delete/
    DATABASE_CANNOT_DELETE_REVIEW = 2200  # Used when a Review cannot be deleted from the database

    # 2210-2219 /review/edit/
    DATABASE_CANNOT_UPDATE_REVIEW = 2210  # Used when a Review cannot be updated in the database

    # Result dictionary used internally only. Empty string for message means no message member is returned
    _result = {

        # 1000-1999
        SUCCESS: 'Success',

        # 9000-9999
        INVALID_PARAMETER: 'Invalid parameter',
        POST_ONLY: 'This method is only accessible by POST',
        GET_ONLY: 'This method is only accessible by GET',
        DATABASE_CANNOT_SAVE: 'Cannot save to database',
        DATABASE_ENTRY_NOT_FOUND: 'Database entry not found',
        DATABASE_MULTIPLE_ENTRIES: 'Expected one entry but found more',

        # 2000-2009
        EMAIL_IN_USE: 'Email already in use',

        # 2010-2019
        DATABASE_CANNOT_UPDATE_USER: 'User cannot be updated in database',

        # 2040-2049
        HYDRA_ERROR: 'Unknown error from Hydra',
        DATABASE_CANNOT_SAVE_ALBUM: 'Album cannot be saved to database',
        DATABASE_CANNOT_SAVE_BLOB: 'Blob cannot be saved to database',
        STORAGE_CANNOT_SAVE_BLOB: 'Blob cannot be saved to storage',
        FILETYPE_INVALID: 'Invalid filetype',
        BLOB_COUNT_INVALID: 'Requested count exceeds available blobs',

        # 2050-2059
        STORAGE_CANNOT_DELETE_BLOB: 'Blob cannot be deleted from storage',
        DATABASE_CANNOT_DELETE_BLOB: 'Blob cannot be deleted from database',
        DATABASE_CANNOT_DELETE_ALBUM: 'Album cannot be deleted from database',

        # 2060-2069
        DATABASE_CANNOT_SAVE_POST: 'Post cannot be saved to database',

        # 2070-2079
        DATABASE_CANNOT_DELETE_POST: 'Post cannot be deleted from database',

        # 2080-2089
        DATABASE_CANNOT_DELETE_ORDER: 'Order cannot be deleted from database',

        # 2090-2099
        ORDER_AMOUNT_EXCEEDS_POST_CAPACITY: 'Order request amount exceeds post capacity',
        DATABASE_CANNOT_SAVE_ORDER: 'Order cannot be saved to database',
        POST_INACTIVE: 'Post inactive',

        # 2100-2109
        DATABASE_CANNOT_SAVE_ORDER_TIME: 'OrderTime cannot be saved to database',

        # 2110-2119
        DATABASE_CANNOT_SAVE_BLOG_POST: 'BlogPost cannot be saved to database',

        # 2120-2129
        DATABASE_CANNOT_DELETE_BLOG_POST: 'BlogPost cannot be deleted from database',

        # 2130-2139
        POST_CAPACITY_INVALID: 'Post capacity invalid',
        DATABASE_CANNOT_UPDATE_POST: 'Post cannot be updated in database',

        # 2140-2149
        DATABASE_CANNOT_UPDATE_USER_LOGIN_PASSWORD: 'Password cannot be updated in database',

        # 2150-2159
        DATABASE_CANNOT_UPDATE_ORDER_STATUS: 'Order status cannot be updated in database',
        ORDER_STATUS_INVALID: 'Invalid order status',
        ORDER_STATUS_POST_EXPIRED: 'Order\'s associated post is expired',

        # 2160-2169
        DATABASE_CANNOT_SAVE_INTERACTION: 'Interaction cannot be saved to database',

        # 2170-2179
        DATABASE_CANNOT_DELETE_INTERACTION: 'Interaction cannot be deleted from database',

        # 2180-2189
        DATABASE_CANNOT_UPDATE_INTERACTION: 'Interaction cannot be updated in database',

        # 2190-2199
        DATABASE_CANNOT_SAVE_REVIEW: 'Review cannot be saved to database',
        RATING_INVALID: 'Invalid rating; must be valid integer between 0 and 10, inclusive',

        # 2200-2209
        DATABASE_CANNOT_DELETE_REVIEW: 'Review cannot be deleted from database',

        # 2210-2220
    }

    @staticmethod
    def append_result(dictionary, result):
        dictionary['result'] = int(result)
        if Result._result.get(int(result)):
            dictionary['message'] = Result._result.get(int(result))

    @staticmethod
    def get_result_dump(result):
        dictionary = {}
        Result.append_result(dictionary, result=int(result))
        return dumps(dictionary)
