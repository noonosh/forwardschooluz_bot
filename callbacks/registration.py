from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ChatAction,
                      KeyboardButton,
                      ReplyKeyboardMarkup)
from callbacks.static.button_texts import *
from callbacks.static import texts
from time import sleep, time
from databases import database_connector as db, select as s
from constants import *
import random
from requests import post
from auth_configs.keys import SMS_URL, SMS_AUTH


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
    try:
        query = update.callback_query
        db.cursor.execute("UPDATE Users SET language = '{}', status = '{}' WHERE id = '{}'".format(
            query.data, LANGUAGE_GOT, s.select_id(update)))
        db.conn.commit()
        query.delete_message()
        context.bot.send_message(chat_id=query.message.chat.id,
                                 text=texts.txt_greeting[query['data']],
                                 parse_mode='HTML')
        request_phone(update, context)
        return PHONE_CONFIRMATION
    except AttributeError:
        pass


def request_phone(update, context):
    button = [
        [KeyboardButton(BTN_PHONE[s.lang(update)], request_contact=True)]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=texts.txt_phone_request[s.lang(update)],
                             reply_markup=ReplyKeyboardMarkup(button,
                                                              resize_keyboard=True),
                             parse_mode='HTML')


def check_phone(update, context):
    headers = {'Content-type': 'application/json',
               'Authorization': f'Basic {SMS_AUTH}'}
    message = update.effective_message
    if update.message.contact or update.message.reply_to_message:
        if message.contact.phone_number[:3] == '998' or update.message.contact.phone_number[1:4] == '998':
            phone = message.contact.phone_number
            code = random.randint(100000, 1000000)
            db.cursor.execute("""UPDATE Users SET phone_number = '{}', code = '{}', status = '{}'
            WHERE telegram_id = '{}'""".format(phone, code, CODE_SENT, message.contact.user_id))
            db.conn.commit()
            buttons = [
                [CHANGE_NUMBER[s.lang(update)]], [RESEND_CODE[s.lang(update)]]
            ]
            body = {
                "messages": [
                    {
                        "recipient": f'{phone}',
                        "message-id": f"{int(time() * 1000000)}",
                        "sms": {
                            "originator": "3700",
                            "content": {
                                "text": f"{texts.sms_text[s.lang(update)].format(code)}"
                            }
                        }
                    }
                ]
            }
            post(SMS_URL, headers=headers, json=body)
            context.bot.send_message(chat_id=message.contact.user_id,
                                     text=f'{texts.code_sent[s.lang(update)]}',
                                     reply_markup=ReplyKeyboardMarkup(buttons,
                                                                      resize_keyboard=True))
            return PHONE_CODE
        else:
            update.effective_message.reply_text(
                texts.phone_country_error[s.lang(update)]
            )
    else:
        message = update.effective_message
        if message.text:
            phone = message.text[1:]
            if phone[:3] == '998' and len(phone) == 12 and int(phone[1:]):
                code = random.randint(100000, 1000000)
                db.cursor.execute("""UPDATE Users SET phone_number = '{}', code = '{}', status = '{}'
                    WHERE telegram_id = '{}'""".format(phone, code, CODE_SENT, message.chat_id))
                db.conn.commit()
                buttons = [
                    [CHANGE_NUMBER[s.lang(update)]], [RESEND_CODE[s.lang(update)]]
                ]
                body = {
                    "messages": [
                        {
                            "recipient": f"{phone}",
                            "message-id": f"{int(time() * 1000000)}",

                            "sms": {
                                "originator": "3700",
                                "content": {
                                    "text": f"{texts.sms_text[s.lang(update)].format(code)}"
                                }
                            }
                        }
                    ]
                }
                post(SMS_URL, headers=headers, json=body)
                update.message.reply_text(f'{texts.code_sent[s.lang(update)]}',
                                          reply_markup=ReplyKeyboardMarkup(buttons,
                                                                           resize_keyboard=True))
                return PHONE_CODE
            else:
                request_phone(update, context)
        else:
            request_phone(update, context)


def check_code(update, context):
    message = update.effective_message
    print(message)
    print('200')


def callback(update, context):
    pass
