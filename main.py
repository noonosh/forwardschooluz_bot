from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

import constants
from auth_configs import keys
from callbacks import registration, starter
from constants import *
import logging
from callbacks.static.texts import *
from callbacks.static.button_texts import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=keys.API_TOKEN)
    dispatcher = updater.dispatcher

    registration_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(registration.greet_user),
                      MessageHandler(Filters.text, registration.greet_user)],
        states={
            PHONE_CONFIRMATION: [
                MessageHandler(Filters.contact | Filters.text, registration.check_phone)
            ],
            PHONE_CODE: {
                MessageHandler(Filters.regex('^' + RESEND_CODE['uz'] + '$') |
                               Filters.regex('^' + RESEND_CODE['ru'] + '$'),
                               registration.check_code),
                MessageHandler(Filters.regex('^' + CHANGE_NUMBER['uz'] + '$') |
                               Filters.regex('^' + CHANGE_NUMBER['ru'] + '$'),
                               registration.check_code),
                MessageHandler(Filters.text, registration.check_code)
            }
        },
        fallbacks=[],
        map_to_parent={
            REG_END: MAIN_MENU
        }
    )

    conversation_main = ConversationHandler(
        entry_points=[CommandHandler('start', starter.start)],
        states={
            REGISTRATION: [registration_conversation]
        },
        fallbacks=[

        ]
    )

    dispatcher.add_handler(conversation_main)

    updater.start_polling()
    updater.idle()
