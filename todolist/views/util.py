"""Holds utility functions."""

import hashlib
import uuid
import pathlib
import todolist


def hash_salt(password, salt=uuid.uuid4().hex):
    """Hash the password with the given salt."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def check_password(password, check):
    """Check one password against another to see if they are equal."""
    spl = check.split('$')
    hash_p = hash_salt(password, spl[1])
    return check == hash_p


def save_picture(fileobj):
    """Save the picture to disk."""
    filename = fileobj.filename

    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = todolist.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    return uuid_basename


def check_user(username):
    """Check whether user is in database."""
    connection = todolist.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = '%s'" % username
    )
    users = cur.fetchall()

    return users


def like_post(username, postid):
    """Request for liking a post."""
    connection = todolist.model.get_db()
    connection.execute(
        "INSERT INTO likes(owner, postid) "
        "VALUES (?, ?)", (username, postid)
    )


def unlike_post(username, postid):
    """Request for unliking a post."""
    connection = todolist.model.get_db()
    connection.execute(
        "DELETE FROM likes "
        "WHERE owner = '%s' "
        "AND postid = '%s' " % (username, postid)
    )


def comment_post(username, postid, text):
    """Request for commenting on a post."""
    connection = todolist.model.get_db()
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?, ?, ?)", (username, postid, text)
    )


def follow_user(username1, username2):
    """Request for following a user."""
    connection = todolist.model.get_db()
    connection.execute(
        "INSERT INTO following(username1, username2) "
        "VALUES (?, ?)", (username1, username2)
    )


def unfollow_user(username1, username2):
    """Request for unfollowing a user."""
    connection = todolist.model.get_db()
    connection.execute(
        "DELETE FROM following "
        "WHERE username1 = '%s' and username2 = '%s' "
        % (username1, username2)
    )


def find_if_liked(username, postid):
    """Request to find if owner liked post."""
    connection = todolist.model.get_db()
    return connection.execute(
        "SELECT COUNT(1) liked "
        "FROM likes "
        "WHERE owner = '%s' AND postid = '%s' " % (username, postid)
    )


def user_action(username, form):
    """Request either like or unlike."""
    if form.get('like', None) is not None:
        like_post(username, form['postid'])
    elif form.get('unlike', None) is not None:
        unlike_post(username, form['postid'])
    elif form.get('comment', None) is not None:
        comment_post(username, form['postid'], form['text'])


def check_list(llama):
    """Check if list exists."""
    if llama:
        return llama[0]
    return {}
