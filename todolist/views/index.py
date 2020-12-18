"""
todolist index (main) view.

URLs include:
/
"""
import flask
import todolist


@todolist.app.route('/')
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)
