"""
todolist index (main) view.

URLs include:
/
"""
import os
import pathlib
import flask
import todolist
from todolist.views.util import hash_salt, check_password, save_picture


@todolist.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Show the login page."""
    # Redirect to index if user is logged in
    if flask.session:
        return flask.redirect(flask.url_for('show_index'))

    if flask.request.method == 'POST':
        connection = todolist.model.get_db()
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = '%s'" % flask.request.form["username"]
        )
        users = cur.fetchall()

        # If the user doesn't exist, abort
        if not users:
            return flask.abort(403)

        # If it is a valid login, create session cookie and redirect
        if check_password(flask.request.form["password"],
                          users[0]['password']):
            flask.session['username'] = flask.request.form['username']
            return flask.redirect(flask.url_for('show_index'))
        # Else, aborts the process and continues
        return flask.abort(403)
    return flask.render_template("login.html")


@todolist.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """Log the user out."""
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('show_login'))


@todolist.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Show the create page."""
    # If the user is logged in, redirect to /accounts/edit/
    if flask.session:
        return flask.redirect(flask.url_for("show_edit"))

    if flask.request.method == 'POST':
        connection = todolist.model.get_db()

        cur = connection.execute(
            "SELECT * "
            "FROM users "
            "WHERE username = '%s'" % flask.request.form["username"]
        )
        users = cur.fetchall()

        # If there is a collision, abort
        if users:
            return flask.abort(409)

        # Password cannot be empty
        if not flask.request.form["password"]:
            return flask.abort(400)

        uuid_basename = save_picture(flask.request.files["file"])

        # Insert the values into the database
        connection.execute(
            "INSERT INTO users(username, fullname, "
            "email, filename, password) "
            "VALUES (?, ?, ?, ?, ?)", (flask.request.form["username"],
                                       flask.request.form["fullname"],
                                       flask.request.form["email"],
                                       uuid_basename,
                                       hash_salt(
                                           flask.request.form["password"])
                                       )
        )

        flask.session['username'] = flask.request.form['username']

        return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("create.html")


@todolist.app.route("/accounts/delete/", methods=["POST", "GET"])
def show_delete():
    """Show the delete page."""
    # If the user is logged in, redirect to /accounts/edit/
    if not flask.session:
        return flask.redirect(flask.url_for("show_login"))
    connection = todolist.model.get_db()
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE owner = '%s'" % flask.session['username']
        )

        links = cur.fetchall()

        for dic in links:
            os.remove(todolist.config.UPLOAD_FOLDER/dic['filename'])

        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = '%s'" % flask.session['username']
        )

        links = cur.fetchall()

        os.remove(todolist.config.UPLOAD_FOLDER/links[0]['filename'])

        connection.execute(
            "DELETE FROM users "
            "WHERE username = '%s'" % flask.session['username']
        )

        flask.session.pop('username', None)
        return flask.redirect(flask.url_for("show_create"))

    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = '%s'" % flask.session['username']
    )

    pic = cur.fetchall()

    return flask.render_template("delete.html",
                                 logname=flask.session['username'],
                                 filename=pic[0]['filename'])


@todolist.app.route("/accounts/edit/", methods=["POST", "GET"])
def show_edit():
    """Show the edit page."""
    if not flask.session:
        return flask.redirect(flask.url_for("show_login"))
    connection = todolist.model.get_db()
    if flask.request.method == "POST":
        if flask.request.files.get('file', None):
            cur = connection.execute(
                "SELECT filename "
                "FROM users "
                "WHERE username = '%s'" % flask.session['username']
            )

            links = cur.fetchall()

            os.remove(todolist.config.UPLOAD_FOLDER/links[0]['filename'])

            uuid_basename = save_picture(flask.request.files["file"])

            connection.execute(
                "UPDATE users "
                "SET filename = ? "
                "WHERE username = ?", (
                    uuid_basename, flask.session['username'])
            )

        connection.execute(
            "UPDATE users "
            "SET fullname = ?, "
            "email = ? "
            "WHERE username = ?", (flask.request.form['fullname'],
                                   flask.request.form['email'],
                                   flask.session['username'])
        )

    cur = connection.execute(
        "SELECT email, fullname, filename "
        "FROM users "
        "WHERE username = '%s'" % flask.session['username']
    )

    temp = cur.fetchall()

    context = {"logname": flask.session['username'],
               "email": temp[0].get('email', None),
               "fullname": temp[0].get('fullname', None),
               "filename": temp[0].get('filename', None)}
    return flask.render_template("edit.html", **context)


@todolist.app.route("/accounts/password/", methods=["POST", "GET"])
def show_password():
    """Show the password page."""
    if not flask.session:
        return flask.redirect(flask.url_for("show_login"))

    if flask.request.method == "POST":
        connection = todolist.model.get_db()
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = '%s'" % flask.session["username"]
        )
        users = cur.fetchall()

        if check_password(flask.request.form['password'],
                          users[0]['password']):
            if flask.request.form['new_password1'] != \
               flask.request.form['new_password2']:
                return flask.abort(401)
            connection.execute(
                "UPDATE users "
                "SET password = ? "
                "WHERE username = ?", (hash_salt(
                    flask.request.form['new_password1']),
                    flask.session['username'])
            )
            return flask.redirect(flask.url_for("show_edit"))
        return flask.abort(403)
    return flask.render_template("password.html",
                                 logname=flask.session['username'])


@todolist.app.route("/uploads/<path:slug>")
def static_permissions(slug):
    """Check for proper access permissions."""
    if not flask.session:
        return flask.abort(403)

    if not pathlib.Path(todolist.config.UPLOAD_FOLDER/slug).is_file():
        return flask.abort(404)

    return flask.send_from_directory(todolist.config.UPLOAD_FOLDER,
                                     slug,
                                     as_attachment=True)
