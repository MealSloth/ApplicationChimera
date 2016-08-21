from databases import databases
import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

PROTOCOL = 'http://'
DOMAIN = 'mealsloth.com'
SUB_DOMAIN_CHIMERA = 'api'
SUB_DOMAIN_HYDRA = 'blob'
URL_CHIMERA = "%s%s.%s/" % (PROTOCOL, SUB_DOMAIN_CHIMERA, DOMAIN,)
URL_HYDRA = "%s%s.%s/" % (PROTOCOL, SUB_DOMAIN_HYDRA, DOMAIN,)

DEBUG = False

ADMINS = (
    ('Michael', 'michael@mealsloth.com'),
)

MANAGERS = ADMINS

DATABASES = databases()

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.mealsloth.com', 'mealsloth-chimera-ap01.appspot.com', ]

SECRET_KEY = '$cl98j&&uh&h5$)zrj(mp62)-$(thx%r4+phj_fh(za6g0al!u'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Chimera.urls'

WSGI_APPLICATION = 'Chimera.wsgi.app'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'Chimera',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

GCS_URL = 'storage.googleapis.com/mealsloth-dryad-bu01/'

# Force using memory for temporary files

FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler', )
FILE_UPLOAD_MAX_MEMORY_SIZE = 5000000
