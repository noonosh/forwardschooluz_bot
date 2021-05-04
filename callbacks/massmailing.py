import time
from presets.actions import restricted
from databases.database_connector import cursor
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction
from telegram.ext import CallbackContext
from callbacks.static.admin_texts import *
from constants import (STATE_ADMIN_MENU,
                       STATE_GET_MEDIA,
                       BECOME_USER,
                       STATE_GET_TEXT,
                       CONFIRM_SENDING)
from callbacks.mainpage import main_page


@restricted
def admin_login(update, context: CallbackContext):
    user_id = update.effective_user.id
    admin = cursor.execute("SELECT name FROM Admins WHERE telegram_id = '{}'"
                           .format(user_id)).fetchone()[0]
    text = "Добро пожаловать в админ панель, {}!"
    context.bot.send_message(chat_id=user_id,
                             text=text.format(admin),
                             reply_markup=ReplyKeyboardRemove())
    payload = {
        'post': {
            'photo': 0,
            'video': 0
        },
        'caption': 0
    }
    context.user_data.update(payload)

    admin_menu(update, context)
    return STATE_ADMIN_MENU


def admin_menu(update, context):
    user_id = update.effective_user.id
    buttons = [
        [KeyboardButton(ADD_MEDIA), KeyboardButton(ADD_TEXT)],
        [KeyboardButton(PREVIEW_IT), KeyboardButton(DELETE_ALL)],
        [KeyboardButton(SEND_ALL)],
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
                             text="Отправьте медиа (фото/видео) для поста",
                             reply_markup=ReplyKeyboardMarkup([[GO_BACK]], resize_keyboard=True))
    return STATE_GET_MEDIA


def save_media(update, context):
    media = update.message
    if media.photo:
        unique_id = media.photo[2].file_unique_id
        f_id = media.photo[2].file_id
        photo = context.bot.get_file(f_id)
        photo.download(f"storage/{unique_id}.jpg")

        payload = {
            "post": {
                "photo": str(unique_id),
                "video": 0
            },
            "caption": 0
        }
        context.user_data.update(payload)

    elif media.video:
        unique_id = media.video.file_unique_id
        f_id = media.video.file_id
        video = context.bot.get_file(f_id)
        context.bot.send_message(chat_id=media.chat.id,
                                 text="Подождите немного...",
                                 reply_markup=ReplyKeyboardRemove())

        video.download(f"storage/{unique_id}.mp4")
        payload = {
            "post": {
                "photo": 0,
                "video": str(unique_id),
            },
            "caption": 0
        }
        context.user_data.update(payload)
    else:
        context.bot.send_message(chat_id=media.chat.id,
                                 text="Принимаются форматы: .jpg/.jpeg/.png или .mp4")
        return

    context.bot.send_message(chat_id=media.chat.id,
                             text="Загружено!")
    back_to_admin_main(update, context)
    return STATE_ADMIN_MENU


def preview_post(update, context):
    chat_id = update.effective_user.id
    try:
        if context.user_data["post"]["photo"] != 0:
            photo = context.user_data['post']['photo']
            context.bot.send_chat_action(chat_id=chat_id,
                                         action=ChatAction.UPLOAD_PHOTO)
            time.sleep(1)

            if context.user_data['caption'] == 0:
                context.bot.send_photo(chat_id=chat_id,
                                       photo=open(f'storage/{photo}.jpg', 'rb'))

            else:
                context.bot.send_photo(chat_id=chat_id,
                                       photo=open(f'storage/{photo}.jpg', 'rb'),
                                       caption=context.user_data['caption'])

        elif context.user_data["post"]["video"] != 0:
            video = context.user_data['post']['video']
            context.bot.send_chat_action(chat_id=chat_id,
                                         action=ChatAction.UPLOAD_VIDEO)
            time.sleep(1)

            if context.user_data['caption'] == 0:
                context.bot.send_video(chat_id=chat_id,
                                       video=open(f'storage/{video}.mp4', 'rb'))

            else:
                context.bot.send_video(chat_id=chat_id,
                                       video=open(f'storage/{video}.mp4', 'rb'),
                                       caption=context.user_data['caption'])

        elif context.user_data['caption'] != 0:
            context.bot.send_chat_action(chat_id=chat_id,
                                         action=ChatAction.TYPING)
            time.sleep(1)

            context.bot.send_message(chat_id=chat_id,
                                     text=context.user_data['caption'])
        else:
            context.bot.send_message(chat_id=chat_id,
                                     text="Пост пустой. Добавьте медиа/текст для начала!")
    except KeyError:
        context.bot.send_message(chat_id=chat_id,
                                 text="Медиа/текст не нашлись. Отправьте сначала медиа/текст")


def get_text(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id,
                             text="Отправьте текст для поста",
                             reply_markup=ReplyKeyboardMarkup([[GO_BACK]], resize_keyboard=True))
    return STATE_GET_TEXT


def save_text(update, context):
    text = update.message.text
    payload = {
        "caption": text
    }
    context.user_data.update(payload)
    context.bot.send_message(chat_id=update.effective_user.id,
                             text='Добавлено!')

    back_to_admin_main(update, context)
    return STATE_ADMIN_MENU


def clear_post(update, context):
    payload = {
        'post': {
            'photo': 0,
            'video': 0
        },
        'caption': 0
    }

    context.user_data.update(payload)
    context.bot.send_message(chat_id=update.effective_user.id,
                             text='Успешно всё очищено!')


def echo_it(update, context):
    get = update.message.text
    update.message.reply_text(get)


def confirm_post(update, context):
    user_id = update.effective_user.id
    if (context.user_data['post']['photo'] == 0
            and context.user_data['post']['video'] == 0
            and context.user_data['caption'] == 0):
        context.bot.send_message(chat_id=user_id,
                                 text="Пост пустой. Добавьте медиа/текст для начала!")
    else:
        buttons = [
            [YES_SEND],
            [NOT_DONT_SEND]
        ]
        context.bot.send_message(chat_id=user_id,
                                 text='Подтвердите, что вы отправляете пост <b>всем!</b>',
                                 parse_mode='HTML',
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return CONFIRM_SENDING


def post_all(update, context):
    context.bot.send_message(chat_id=update.effective_user.id,
                             text='Начинаю рассылку...\n\nНе пользуйтесь ботом пока доставлю сообщения до всех!',
                             reply_markup=ReplyKeyboardRemove())
    users_ids = cursor.execute("""SELECT telegram_id from Users
    EXCEPT SELECT telegram_id FROM Users WHERE telegram_id = '{}'""".format(update.effective_user.id)).fetchall()

    for i in users_ids:
        if context.user_data["post"]["photo"] != 0:
            photo = context.user_data['post']['photo']

            if context.user_data['caption'] == 0:
                context.bot.send_photo(chat_id=i[0],
                                       photo=open(f'storage/{photo}.jpg', 'rb'))
                time.sleep(0.05)

            else:
                context.bot.send_photo(chat_id=i[0],
                                       photo=open(f'storage/{photo}.jpg', 'rb'),
                                       caption=context.user_data['caption'])
                time.sleep(0.05)

        elif context.user_data["post"]["video"] != 0:
            video = context.user_data['post']['video']

            if context.user_data['caption'] == 0:
                context.bot.send_video(chat_id=i[0],
                                       video=open(f'storage/{video}.mp4', 'rb'))
                time.sleep(0.05)

            else:
                context.bot.send_video(chat_id=i[0],
                                       video=open(f'storage/{video}.mp4', 'rb'),
                                       caption=context.user_data['caption'])
                time.sleep(0.05)

        elif context.user_data['caption'] != 0:
            context.bot.send_message(chat_id=i[0],
                                     text=context.user_data['caption'])
            time.sleep(0.05)

    context.bot.send_message(chat_id=update.effective_user.id,
                             text='Рассылка была успешно доставлена всем!')
    main_page(update, context)
    return BECOME_USER


def ignore(update, context):
    return


def quit_admin_panel(update, context):
    main_page(update, context)
    return BECOME_USER
