import time
from functools import wraps
from databases.database_connector import cursor, conn


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            time.sleep(0.5)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        a = cursor.execute("SELECT telegram_id FROM Admins"
                           .format(user_id)).fetchall()
        ADMINS = []
        for i in a:
            ADMINS.append(i[0])
        if user_id not in ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped
