"""
todolist index (main) view.

URLs include:
/
"""
import flask
import todolist


@todolist.app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    """Display / route."""

    if not flask.session:
        return flask.redirect(flask.url_for('show_login'))

    if flask.request.method == 'POST':
        # Connect to database
        connection = todolist.model.get_db()

        # Query database
        connection.execute(
            "INSERT INTO tasks(owner, text, duedate) "
            "VALUES(?, ?, ?)", (flask.request.form['username'], flask.request.form['task'], flask.request.form['duedate'])
        )
        flask.redirect(flask.url_for('show_index'))

    context = {}
    return flask.render_template("newpost.html", **context)
