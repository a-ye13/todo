"""TODOlist development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (b'\xfe\x81\x84\x1bn\xcd\xc3\xdbu \
        \x9f^\xa6\xf8\x96\x01y\xec\x1cZG\x16g\xbf\x0b')
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
TODOLIST_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = TODOLIST_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/todo.sqlite3
DATABASE_FILENAME = TODOLIST_ROOT/'var'/'todo.sqlite3'
