
APP_NAME = 'strappo-analytics'
TAG = '0.0.1'

DEBUG = False

DEV = False

LOGGER_NAME = APP_NAME
LOG_ENABLE = True
LOG_FORMAT = '[%(process)d] %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'

API_HOST = "127.0.0.1:8000"


try:
    from local_config import *
except ImportError:
    pass
