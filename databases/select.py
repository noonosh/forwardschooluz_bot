from databases import database_connector as db


def select_all(update):
    """Returns a list."""
    chat_id = update.effective_chat.id
    user = db.cursor.execute("SELECT * from Users WHERE telegram_id = '{}'".format(chat_id)).fetchall()
    return user


def select_id(update):
    """Returns an instance."""
    chat_id = update.effective_chat.id
    user = db.cursor.execute("SELECT id from Users WHERE telegram_id = '{}'".format(chat_id)).fetchone()
    return user[0]


def select_state(update):
    a = db.cursor.execute("SELECT status FROM Users WHERE id = '{}'".format(select_id(update))).fetchone()[0]
    return a


def lang(update):
    language = db.cursor.execute("SELECT language from Users WHERE id = '{}'".format(select_id(update))).fetchone()
    return language[0]
