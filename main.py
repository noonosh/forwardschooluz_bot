from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    PollAnswerHandler,
    PicklePersistence
)
from ptbcontrib.reply_to_message_filter import ReplyToMessageFilter

from error_sender import error_handler
from callbacks.mainpage import *
from auth_configs import keys
from callbacks import (registration, starter, kiosk, livegram, markups,
                       section_settings,
                       section_test, videos)
from constants import *
from callbacks.static.button_texts import *


def main():
    persistence = PicklePersistence(filename='RESTRICTED')
    updater = Updater(token=keys.API_TOKEN, persistence=persistence, use_context=True)
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

    quiz_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(section_test.quiz_getting_started, pattern='start_that_quiz')],
        states={
            TEST_PROCESS: [
                PollAnswerHandler(section_test.send_questions)
            ]
        },
        fallbacks=[],
        per_chat=False
    )

    conversation_main = ConversationHandler(
        entry_points=[CommandHandler('start', starter.start),
                      MessageHandler(Filters.regex(SUBMIT_QUIZ_RESULTS['uz']) |
                                     Filters.regex(SUBMIT_QUIZ_RESULTS['ru']), section_test.completed_quiz)],
        states={
            # RESPONSE_GROUP: [
            #     MessageHandler(ReplyToMessageFilter(Filters.user(1148622134)), livegram.reply_to_user)
            # ],
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
                               Filters.regex(BACK['ru']), main_page)
            ],
            ASKING: [
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), markups.ask_me_markup),
                MessageHandler(Filters.text |
                               Filters.photo |
                               Filters.voice |
                               Filters.audio |
                               Filters.document, livegram.forward)
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
                               Filters.regex(BACK['ru']), back_to_main),

                MessageHandler(Filters.photo, kiosk.get_photo_id)
            ],
            I_WANT_TO_WATCH: [
                MessageHandler(Filters.regex(VIDEO_1['uz']) |
                               Filters.regex(VIDEO_1['ru']), videos.video_1),
                MessageHandler(Filters.regex(VIDEO_2['uz']) |
                               Filters.regex(VIDEO_2['ru']), videos.video_2),
                MessageHandler(Filters.regex(VIDEO_3['uz']) |
                               Filters.regex(VIDEO_3['ru']), videos.video_3),
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main),
                MessageHandler(Filters.video, videos.get_video_id)
            ],
            I_WANT_A_TEST: [
                MessageHandler(Filters.regex(I_HAVE_KEY['uz']) |
                               Filters.regex(I_HAVE_KEY['ru']), section_test.test_key),
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ],
            TEST_READY_STATE: [
                MessageHandler(Filters.text, section_test.check_key)
            ],
            CONFIGURATIONS_PLEASE: [
                MessageHandler(Filters.regex(CHANGE_LANG['uz']) |
                               Filters.regex(CHANGE_LANG['ru']), section_settings.change_language),
                MessageHandler(Filters.regex(BACK['uz']) |
                               Filters.regex(BACK['ru']), back_to_main)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.all & (~ Filters.user(1148622134)), starter.reset),
            CommandHandler('reset', starter.reset)
        ],
        persistent=True,
        name='my_conversation'
    )

    dispatcher.add_handler(conversation_main)
    dispatcher.add_handler(quiz_conversation)
    dispatcher.add_handler(MessageHandler(ReplyToMessageFilter(Filters.user(1148622134)), livegram.reply_to_user))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
