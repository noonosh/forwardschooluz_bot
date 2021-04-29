from user_settings import *
from databases.select import lang
from callbacks.static.texts import intensive_6_txt, intensive_7_txt, general_english_txt, ielts_txt
from callbacks.mainpage import back_to_main


def intensive_6(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_photo(chat_id=telegram_id,
                           photo=INTENSIVE_6_PHOTO)
    update.message.reply_html(intensive_6_txt[lang(update)])


def intensive_7(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_photo(chat_id=telegram_id,
                           photo=INTENSIVE_7_PHOTO)
    update.message.reply_html(intensive_7_txt[lang(update)])


def general(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_photo(chat_id=telegram_id,
                           photo=GENERAL_ENGLISH_PHOTO)
    update.message.reply_html(general_english_txt[lang(update)])


def ielts(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_photo(chat_id=telegram_id,
                           photo=IELTS_PHOTO)
    update.message.reply_html(ielts_txt[lang(update)])


def get_photo_id(update, context):
    telegram_id = update.message.chat_id
    if telegram_id in ADMIN_IDS:
        context.bot.send_message(chat_id=telegram_id,
                                 text=update.message.photo[0].file_id)
    else:
        back_to_main(update, context)
