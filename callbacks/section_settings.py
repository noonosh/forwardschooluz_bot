from databases.select import select_id, lang
from databases.database_connector import conn, cursor
from callbacks.mainpage import main_page
from constants import MAIN_MENU


def change_language(update, context):
    if lang(update) == 'uz':
        cursor.execute(
            "UPDATE Users SET language = 'ru' WHERE id = '{}'".format(select_id(update)))
        conn.commit()
    if lang(update) == 'ru':
        cursor.execute(
            "UPDATE Users SET language = 'uz' WHERE id = '{}'".format(select_id(update)))
        conn.commit()
    main_page(update, context)
    return MAIN_MENU

