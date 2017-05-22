# coding: utf-8

"""
Quokka will try to read configurations from environment variables
so you dont need this local_settings.py file if you have env vars.

1. You can set as a file

export QUOKKA_SETTINGS='/path/to/settings.py'

2. You can set individual values

export QUOKKA_MONGODB_DB="quokka_db"
export QUOKKA_MONGODB_HOST='localhost'
export QUOKKA_MONGODB_PORT='$int 27017'

Or just fill your values in this file and rename it to 'local_settings.py'
"""
from quokka.utils.settings import get_password
import os

MONGODB_DB = "quokka_db"

heroku_mongo_uri = os.environ.get('MONGODB_URI',None)

if heroku_mongo_uri is not None:
    MONGODB_HOST = heroku_mongo_uri
else:
# MONGO
    MONGODB_HOST = 'ds135700.mlab.com'
    MONGODB_PORT = 35700
    MONGODB_USERNAME = 'quokka_osx'
    MONGODB_PASSWORD = 'quokka_osx'
    MONGODB_DB = 'quokka'

# Debug and toolbar
DEBUG = False
DEBUG_TB_ENABLED = False
DEBUG_TOOLBAR_ENABLED = True


# set this to true in development mode
if DEBUG:
    ADMIN_RAISE_ON_VIEW_EXCEPTION = True


# locale
BABEL_DEFAULT_LOCALE = 'en'

# Logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'


"""
If you want to have a new theme installed you can use quokkacms tool
    $ pip install quokkacms
    $ cd quokka
    $ quokkacms install_theme material
The above commands will download material design theme to your themes folder,
then just enable it.
"""
DEFAULT_THEME = 'uikit'
ADMIN_THEME = 'admin'

SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True

SIDEBAR_COLOR = "blue"

ADMIN_RAISE_ON_VIEW_EXCEPTION = True

ADMIN = dict(
    name="My BaddAss Admin",
    url="/admin",
)

ADMIN_EXTRA_VIEWS = [
    dict(
        module="quokka.modules.cart.admin.AddNewProductAdmin",
        category="Cart",
        name="AddProducts",
    ),
    dict(
       module='quokka.core.admin.views.ProcessFileAddView',       
       category=None,
       name='brioken badd',
    ),
]

CODEMIRROR_LANGUAGES = ['jinja2','django','python', 'htmlmixed','javascript','css','xml']
CODEMIRROR_VERSION = '5.25.0'
# optional
CODEMIRROR_THEME = 'vibrant-ink'
CODEMIRROR_ADDONS = (
            ('display','placeholder'),
            ('mode','overlay'),
            ('hint','show-hint'),
            ('hint','xml-hint'),
            ('hint','html-hint')
)

EXTRA_EXTENSIONS = [
    'flask.ext.codemirror.CodeMirror',
    'flask_wtf.CsrfProtect',
]


"""
Emails go to shell until you configure this
http://pythonhosted.org/Flask-Mail/
"""
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
# MAIL_USE_SSL = True
MAIL_USE_TLS = True
MAIL_USERNAME = 'jstacoder@gmail.com'
# Create a .email_password.txt in ../
MAIL_PASSWORD = get_password('email')
DEFAULT_MAIL_SENDER = 'jstacoder@gmail.com'

