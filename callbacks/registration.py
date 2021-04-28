from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ChatAction,
                      KeyboardButton,
                      ReplyKeyboardMarkup,
                      ReplyKeyboardRemove)
from callbacks.static.button_texts import *
from callbacks.static import texts
from time import sleep, time
from databases.database_connector import *
from databases.select import *
from constants import *
import random
from requests import post
from auth_configs.keys import SMS_URL, SMS_AUTH
from callbacks.mainpage import main_page


def choose_language(update, context):
    message = update.message
    buttons = [
        [InlineKeyboardButton(BTN_UZ, callback_data='uz'),
         InlineKeyboardButton(BTN_RU, callback_data='ru')]
    ]
    image = open("assets/images/hello.png", 'rb')
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                 action=ChatAction.UPLOAD_PHOTO)
    sleep(0.5)
    context.bot.send_photo(chat_id=message.chat_id,
                           photo=image,
                           caption=texts.txt_choose_lang,
                           reply_markup=InlineKeyboardMarkup(buttons))


def greet_user(update, context):
    # try-else block here allows us to ignore messages from user,
    # which are not CallbackQueryAnswers

    try:
        query = update.callback_query
        query.answer()
        cursor.execute("UPDATE Users SET language = '{}', status = '{}' WHERE id = '{}'".format(
            query.data, LANGUAGE_GOT, select_id(update)))
        conn.commit()
        query.delete_message()
        context.bot.send_message(chat_id=query.message.chat.id,
                                 text=texts.txt_greeting[query['data']],
                                 parse_mode='HTML')
        request_phone(update, context)
        return PHONE_CONFIRMATION
    except AttributeError as e:
        print(e)


def request_phone(update, context):
    button = [
        [KeyboardButton(BTN_PHONE[lang(update)], request_contact=True)]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=texts.txt_phone_request[lang(update)],
                             reply_markup=ReplyKeyboardMarkup(button,
                                                              resize_keyboard=True),
                             parse_mode='HTML')
    return PHONE_CONFIRMATION


def check_phone(update, context):
    headers = {'Content-type': 'application/json',
               'Authorization': f'Basic {SMS_AUTH}'}
    message = update.effective_message
    if update.message.contact or update.message.reply_to_message:
        if message.contact.phone_number[:3] == '998' or update.message.contact.phone_number[1:4] == '998':
            phone = message.contact.phone_number
            code = random.randint(100000, 1000000)
            cursor.execute("""UPDATE Users SET phone_number = '{}', code = '{}', status = '{}'
            WHERE telegram_id = '{}'""".format(phone, code, CODE_SENT, message.contact.user_id))
            conn.commit()
            buttons = [
                [CHANGE_NUMBER[lang(update)]], [RESEND_CODE[lang(update)]]
            ]
            body = {
                "messages": [
                    {
                        "recipient": f'{phone}',
                        "message-id": f"{int(time() * 1000000)}",
                        "sms": {
                            "originator": "3700",
                            "content": {
                                "text": f"{texts.sms_text[lang(update)].format(code)}"
                            }
                        }
                    }
                ]
            }
            post(SMS_URL, headers=headers, json=body)
            context.bot.send_message(chat_id=message.contact.user_id,
                                     text=f'{texts.code_sent[lang(update)]}',
                                     reply_markup=ReplyKeyboardMarkup(buttons,
                                                                      resize_keyboard=True))
            return PHONE_CODE
        else:
            update.effective_message.reply_text(
                texts.phone_country_error[lang(update)]
            )
    else:
        message = update.effective_message
        if message.text:
            phone = message.text[1:]
            if phone[:3] == '998' and len(phone) == 12 and int(phone[1:]):
                code = random.randint(100000, 1000000)
                cursor.execute("""UPDATE Users SET phone_number = '{}', code = '{}', status = '{}'
                    WHERE telegram_id = '{}'""".format(phone, code, CODE_SENT, message.chat_id))
                conn.commit()
                buttons = [
                    [CHANGE_NUMBER[lang(update)]], [RESEND_CODE[lang(update)]]
                ]
                body = {
                    "messages": [
                        {
                            "recipient": f"{phone}",
                            "message-id": f"{int(time() * 1000000)}",

                            "sms": {
                                "originator": "3700",
                                "content": {
                                    "text": f"{texts.sms_text[lang(update)].format(code)}"
                                }
                            }
                        }
                    ]
                }
                post(SMS_URL, headers=headers, json=body)
                update.message.reply_text(f'{texts.code_sent[lang(update)]}',
                                          reply_markup=ReplyKeyboardMarkup(buttons,
                                                                           resize_keyboard=True))
                return PHONE_CODE
            else:
                request_phone(update, context)
        else:
            request_phone(update, context)


def check_code(update, context):
    message = update.effective_message
    code = cursor.execute("SELECT code FROM Users WHERE telegram_id = '{}'"
                          .format(message.chat_id)).fetchone()[0]
    try:
        if int(message.text) == code:
            cursor.execute("UPDATE Users SET status = '{}' WHERE telegram_id = '{}'"
                           .format(PHONE_CONFIRMED, message.chat_id))
            conn.commit()
            name_request(update, context)
            return NAME_INPUT
        else:
            update.effective_message.reply_text(texts.code_error[lang(update)])
    except ValueError:
        update.effective_message.reply_text(texts.code_error[lang(update)])


def resend_code(update, context):
    chat_id = update.effective_chat.id
    code = random.randint(100000, 1000000)
    cursor.execute("UPDATE Users SET code = '{}' WHERE telegram_id = '{}'".format(code, chat_id))
    conn.commit()
    phone_num = cursor.execute(
        "SELECT phone_number FROM Users WHERE telegram_id = '{}'".format(chat_id)).fetchone()
    headers = {'Content-type': 'application/json',
               'Authorization': f'Basic {SMS_AUTH}'}
    body = {
        "messages": [
            {
                "recipient": f"{phone_num[0]}",
                "message-id": f"{int(time() * 1000000)}",

                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": f"{texts.sms_text[lang(update)].format(code)}"
                    }
                }
            }
        ]
    }
    post(SMS_URL, headers=headers, json=body)
    update.message.reply_text(f'{texts.code_resent[lang(update)]}')


def name_request(update, context):
    update.message.reply_text(texts.txt_name_request[lang(update)],
                              reply_markup=ReplyKeyboardRemove())


def name_accept(update, context):
    message = update.effective_message
    a = message.text.split()
    if len(a) == 2:  # Check if the user has entered TWO words ONLY!

        if a[0][0].isupper() and a[1][0].isupper():

            cursor.execute('''UPDATE Users SET name = '{}', status = '{}'
                WHERE telegram_id = '{}' '''.format(message.text, ACTIVE_USER, update.message.chat_id))
            conn.commit()
            message.reply_text(texts.name_accepted[lang(update)])

            main_page(update, context)  # MAIN MENU SHOULD BE DISPLAYED HERE

            return REG_END
        else:
            update.message.reply_text(texts.name_error_2[lang(update)])
    else:
        update.message.reply_text(texts.name_error_1[lang(update)])
