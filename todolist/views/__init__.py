"""Views, one for each Insta485 page."""
from todolist.views.index import show_index

from todolist.views.accounts import show_login
from todolist.views.accounts import show_create
from todolist.views.accounts import show_delete
from todolist.views.accounts import show_edit
from todolist.views.accounts import show_logout

from todolist.views.newpost import new_post