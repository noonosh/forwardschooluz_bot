from telegram import ReplyKeyboardMarkup, ChatAction
from callbacks.static.button_texts import *
from callbacks.static.texts import *
from databases.select import lang
from constants import *


def main_page(update, context) -> None:
    markup = ReplyKeyboardMarkup(
        [
            [ASK_ME[lang(update)]],

            [GET_INFO[lang(update)]],

            [TEST_KNOWLEDGE[lang(update)], WATCH_VIDEO[lang(update)]],

            [SETTINGS[lang(update)]]
        ],
        resize_keyboard=True
    )

    update.effective_message.reply_text(main_menu_markup[lang(update)],
                                        reply_markup=markup)
    return MAIN_MENU


def back_to_main(update, context):
    main_page(update, context)
    return MAIN_MENU
