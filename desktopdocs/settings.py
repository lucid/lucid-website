from desktopsite.settings import *

PREPEND_WWW = False
APPEND_SLASH = True
INSTALLED_APPS = ['desktopdocs', 'dojango']
TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "templates")] + list(TEMPLATE_DIRS)
TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request']
ROOT_URLCONF = 'desktopdocs.urls'
CACHE_MIDDLEWARE_KEY_PREFIX = 'desktopdocs'

DOCS_PICKLE_ROOT = "/var/www/desktop/desktopdev/documentation/_build/pickle/"
