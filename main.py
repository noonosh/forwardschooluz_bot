from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    PollAnswerHandler,
    PollHandler
)

from callbacks.mainpage import *
from auth_configs import keys
from callbacks import (registration, starter, kiosk, livegram, markups,
                       section_settings,
                       section_test)
from constants import *
import logging
from callbacks.static.button_texts import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=keys.API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    registration_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='uz', callback=registration.greet_user),
                      CallbackQueryHandler(pattern='ru', callback=registration.greet_user),
                      MessageHandler(Filters.text, registration.greet_user)],
        states={
            PHONE_CONFIRMATION: [
                MessageHandler(Filters.contact | Filters.text, registration.check_phone)
            ],
            PHONE_CODE: [
                MessageHandler(Filters.regex('^' + RESEND_CODE['uz'] + '$') |
                               Filters.regex('^' + RESEND_CODE['ru'] + '$'),
                               registration.resend_code),

                MessageHandler(Filters.regex('^' + CHANGE_NUMBER['uz'] + '$') |
                               Filters.regex('^' + CHANGE_NUMBER['ru'] + '$'),
                               registration.request_phone),

                MessageHandler(Filters.text, registration.check_code)
            ],
            NAME_INPUT: [
                MessageHandler(Filters.text, registration.name_accept)
            ]
        },
        fallbacks=[],
        map_to_parent={
            REG_END: MAIN_MENU
        }
    )

    placement_test_conversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(I_HAVE_KEY['uz']) |
                                     Filters.regex(I_HAVE_KEY['ru']), section_test.test_key)],
        states={
            TEST_AUTH: [
                MessageHandler(Filters.text, section_test.check_key)
            ],
            TEST_READY_STATE: [
                CallbackQueryHandler(section_test.quiz_getting_started, pattern='start_that_quiz')
            ],
            TEST_PROCESS: [
                PollAnswerHandler(section_test.send_questions)
            ],
            TEST_OVERVIEW_STATE: [
                MessageHandler(Filters.regex(SUBMIT_QUIZ_RESULTS['uz']) |
                               Filters.regex(SUBMIT_QUIZ_RESULTS['ru']), section_test.completed_quiz)
            ]
        },
        fallbacks=[],
        per_chat=False,
        map_to_parent={
            MAIN_MENU: MAIN_MENU
        }
    )

    conversation_main = ConversationHandler(
        entry_points=[CommandHandler('start', starter.start)],
        states={
            REGISTRATION: [registration_conversation],
            MAIN_MENU: [
                MessageHandler(Filters.regex(ASK_ME['uz']) |
                               Filters.regex(ASK_ME['ru']), markups.ask_me_markup),

                MessageHandler(Filters.regex(GET_INFO['uz']) |
                               Filters.regex(GET_INFO['ru']), markups.get_info_markup),

                MessageHandler(Filters.regex(WATCH_VIDEO['uz']) |
                               Filters.regex(WATCH_VIDEO['ru']), markups.watch_video_markup),

                MessageHandler(Filters.regex(TEST_KNOWLEDGE['uz']) |
                               Filters.regex(TEST_KNOWLEDGE['ru']), markups.placement_test_markup),

                MessageHandler(Filters.regex(SETTINGS['uz']) |
                               Filters.regex(SETTINGS['ru']), markups.settings_markup)
            ],
            I_HAVE_A_QUESTION: [
                MessageHandler(Filters.regex(ASK_SUPPORT['uz']) |
                               Filters.regex(ASK_SUPPORT['ru']) |
                               Filters.regex(ASK_TEACHER['uz']) |
                               Filters.regex(ASK_TEACHER['ru']) |
                               Filters.regex(ASK_ADMINISTRATION['uz']) |
                               Filters.regex(ASK_ADMINISTRATION['ru']) |
                               Filters.regex(ASK_FINANCE['uz']) |
                               Filters.regex(ASK_FINANCE['ru']), livegram.ask),

                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ],
            I_WANT_TO_GET_INFO: [
                MessageHandler(
                    Filters.regex(INTENSIVE_6['uz']) |
                    Filters.regex(INTENSIVE_6['ru']), kiosk.intensive_6),
                MessageHandler(
                    Filters.regex(INTENSIVE_7['uz']) |
                    Filters.regex(INTENSIVE_7['ru']), kiosk.intensive_7),
                MessageHandler(
                    Filters.regex(GENERAL_ENGLISH['uz']) |
                    Filters.regex(GENERAL_ENGLISH['ru']), kiosk.general),
                MessageHandler(
                    Filters.regex(IELTS['uz']) |
                    Filters.regex(IELTS['ru']), kiosk.ielts),

                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
                # MessageHandler(Filters.photo, get_photo_id)
            ],
            I_WANT_TO_WATCH: [
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ],
            I_WANT_A_TEST: [
                placement_test_conversation,
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ],
            CONFIGURATIONS_PLEASE: [
                MessageHandler(Filters.regex(CHANGE_LANG['uz']) |
                               Filters.regex(CHANGE_LANG['ru']), section_settings.change_language),
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ]
        },
        fallbacks=[

        ],
        per_chat=False
    )

    dispatcher.add_handler(conversation_main)

    updater.start_polling()
    updater.idle()
