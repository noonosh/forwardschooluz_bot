import time
from presets.actions import restricted
from databases.database_connector import cursor
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from callbacks.static.admin_texts import *
from constants import STATE_ADMIN_MENU, STATE_GET_MEDIA


@restricted
def admin_login(update, context: CallbackContext):
    user_id = update.effective_user.id
    admin = cursor.execute("SELECT name FROM Admins WHERE telegram_id = '{}'"
                           .format(user_id)).fetchone()[0]
    text = "Добро пожаловать в админ панель, {}!"
    context.bot.send_message(chat_id=user_id,
                             text=text.format(admin),
                             reply_markup=ReplyKeyboardRemove())
    admin_menu(update, context)
    return STATE_ADMIN_MENU


def admin_menu(update, context):
    user_id = update.effective_user.id
    buttons = [
        [KeyboardButton(ADD_PHOTO), KeyboardButton(ADD_TEXT)],
        [KeyboardButton(PREVIEW_IT), KeyboardButton(SEND_ALL)],
        [KeyboardButton(EXIT_ADMIN)]
    ]
    context.bot.send_message(chat_id=user_id,
                             text=choose_action,
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def back_to_admin_main(update, context):
    admin_menu(update, context)
    return STATE_ADMIN_MENU


def get_media(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id,
                             text="Отправьте медиа (фото, видео) для поста",
                             reply_markup=ReplyKeyboardMarkup([[GO_BACK]], resize_keyboard=True))
    return STATE_GET_MEDIA


def save_media(update, context):
    media = update.message
    unique_id = media.photo[2].file_unique_id
    f_id = media.photo[2].file_id
    photo = context.bot.get_file(f_id)
    photo.download(f"storage/{unique_id}.jpg")
    context.bot.send_message(chat_id=media.chat.id,
                             text="Отлично!")
    payload = {
        "post": {
            "photo": str(unique_id)
        }
    }
    context.bot_data.update(payload)
    back_to_admin_main(update, context)
    return STATE_ADMIN_MENU


def preview_post(update, context):
    chat_id = update.effective_user.id
    media = context.bot_data['post']['photo']
    context.bot.send_photo(chat_id=chat_id,
                           photo=open(f'storage/{media}.jpg', 'rb'))


def echo_it(update, context):
    get = update.message.text
    update.message.reply_text(get)


def post(update, context):
    users_ids = cursor.execute("SELECT telegram_id from Users").fetchall()
    for i in users_ids:
        context.bot.send_message(chat_id=i[0],
                                 text='This is a mass mailing')
        time.sleep(4)
