"""
todolist index (main) view.

URLs include:
/
"""
import flask
import todolist


@todolist.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""

    if not flask.session:
        return flask.redirect(flask.url_for('show_login'))

    if flask.request.method == 'POST':
        if flask.request.form["submit_button"] == "Add new task":
            return flask.redirect(flask.url_for("new_post"))

    # Connect to database
    connection = todolist.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT owner, text, duedate "
        "FROM tasks"
    )
    tasks = cur.fetchall()

    # Add database info to context
    context = {"tasks": tasks}
    return flask.render_template("index.html", **context)
