# Django settings for desktopsite project.
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('HFLW', 'me@hflw.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'desktop.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SITE_ROOT = "http://www.lucid-project.org/"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ROOT_PATH = "/home/HFLW/Projects/lucid/website/trunk/desktopsite"

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/media/' % ROOT_PATH

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sf+y41ck7n-y2^w($$e18hwl3$ei1682gr$3b7wvh1cbr)k&5='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",

    # SNAPboard processors
    "desktopsite.apps.snapboard.views.snapboard_default_context",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'desktopsite.apps.snapboard.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'desktopsite.urls'

TEMPLATE_DIRS = (
    "%s/templates/" % ROOT_PATH,
    "%s/dojango/templates/" % ROOT_PATH,
    "%s/apps/blog/templates/" % ROOT_PATH,
    "%s/apps/content/templates/" % ROOT_PATH,
    "%s/apps/accounts/templates/" % ROOT_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.admin',
    'desktopsite.apps.snapboard',
    'desktopsite.apps.comment_utils',
    'desktopsite.apps.blog',
    'desktopsite.apps.content',
    'dojango',
)

### SNAPBOARD ###
SNAP_PREFIX = "/forum";
SNAP_MEDIA_PREFIX = MEDIA_URL + '/forum'


### DOJANGO ###
DOJANGO_DOJO_DEBUG = False