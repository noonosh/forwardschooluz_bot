from databases import database_connector as db, select
from callbacks import registration
from constants import *


def start(update, context):
    user = update.message.chat
    if user.id < 0:
        pass  # in GROUP
    elif user.id > 0:
        if len(select.select_all(update)) == 0:
            db.cursor.execute("""INSERT INTO Users (
            telegram_id,
            name,
            username,
            phone_number,
            code,
            status
            ) VALUES (
            '{}',
            '{}',
            '{}',
            NULL,
            NULL,
            '{}')""".format(
                user.id,
                user.first_name + ' ' + user.last_name,
                user.username,
                NEW_USER))
            db.conn.commit()
            registration.choose_language(update, context)
            return REGISTRATION
        else:
            if select.select_state != ACTIVE_USER:
                db.cursor.execute("DELETE FROM Users WHERE id = '{}'".format(select.select_id(update)))
                db.conn.commit()
                start(update, context)
                return REGISTRATION
            elif select.select_state == ACTIVE_USER:
                pass  # MAIN PAGE

    else:
        raise Exception("No telegram ID was determined during the update.")
