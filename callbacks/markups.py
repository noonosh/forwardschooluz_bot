from constants import *
from callbacks.static.button_texts import *
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from databases.select import lang
from callbacks.static.texts import amm_text, gim_text, wvm_text, ptm_text, settings_markup_text


def ask_me_markup(update, context):
    menu = ReplyKeyboardMarkup(

        [[ASK_SUPPORT[lang(update)]],

         [ASK_TEACHER[lang(update)]],

         [ASK_ADMINISTRATION[lang(update)]],

         [ASK_FINANCE[lang(update)]],

         [BACK[lang(update)]]

         ], resize_keyboard=True)
    update.effective_message.reply_text(
        text=amm_text[lang(update)],
        reply_markup=menu)
    return I_HAVE_A_QUESTION


def get_info_markup(update, context):
    menu = ReplyKeyboardMarkup(

        [[INTENSIVE_6[lang(update)], INTENSIVE_7[lang(update)]],

         [GENERAL_ENGLISH[lang(update)]],

         [IELTS[lang(update)]],

         [BACK[lang(update)]]

         ], resize_keyboard=True)
    update.effective_message.reply_text(gim_text[lang(update)],
                                        reply_markup=menu)
    return I_WANT_TO_GET_INFO


def watch_video_markup(update, context):
    menu = ReplyKeyboardMarkup(

        [[VIDEO_1[lang(update)]],

         [VIDEO_2[lang(update)], VIDEO_3[lang(update)]],

         [BACK[lang(update)]]

         ], resize_keyboard=True)
    update.effective_message.reply_text(wvm_text[lang(update)],
                                        reply_markup=menu)
    return I_WANT_TO_WATCH


def placement_test_markup(update, context):
    menu = ReplyKeyboardMarkup(
        [
            [I_HAVE_KEY[lang(update)]],
            [BACK[lang(update)]]
        ],
        resize_keyboard=True
    )
    update.effective_message.reply_text(ptm_text[lang(update)],
                                        reply_markup=menu,
                                        parse_mode='HTML')
    return I_WANT_A_TEST


def settings_markup(update, context):
    menu = ReplyKeyboardMarkup(
        [
            [CHANGE_LANG[lang(update)]],
            [BACK[lang(update)]]
        ],
        resize_keyboard=True
    )
    update.effective_message.reply_text(settings_markup_text[lang(update)],
                                        reply_markup=menu)
    return CONFIGURATIONS_PLEASE
