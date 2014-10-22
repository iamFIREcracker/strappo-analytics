
APP_NAME = 'strappo-analytics'
TAG = '0.0.1'

DEBUG = False
DEBUG_SQL = False

DEV = False

LOGGER_NAME = APP_NAME
LOG_ENABLE = True
LOG_FORMAT = '[%(process)d] %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'

DISABLE_HTTP_ACCEPT_CHECK = False

DATABASE_URL = 'sqlite:///appdb.sqlite'

SECRET = "ohmygodlookatthetree"


try:
    from local_config import *
except ImportError:
    pass
