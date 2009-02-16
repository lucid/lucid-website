from desktopsite.settings import *

PREPEND_WWW = False
APPEND_SLASH = True
INSTALLED_APPS = ['desktopdocs']
TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "templates")] + list(TEMPLATE_DIRS)
TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request']
ROOT_URLCONF = 'desktopdocs.urls'
CACHE_MIDDLEWARE_KEY_PREFIX = 'desktopdocs'

if DEVELOPMENT_MODE:
    DOCS_PICKLE_ROOT = "/Users/jacob/Projects/Django/upstream/docs/_build/pickle/"
else:
    DOCS_PICKLE_ROOT = "/home/jacob/django-docs/docs/_build/pickle"
