from constants import ASKING, I_HAVE_A_QUESTION
from databases.select import lang
from databases.database_connector import cursor
from telegram import ReplyKeyboardMarkup
from callbacks.markups import ask_me_markup
from callbacks.static.button_texts import BACK
from callbacks.static.texts import asking_texts, gotcha_texts, txt_reply


def ask(update, context):
    target_group = update.effective_message.text
    group_id = cursor.execute("SELECT group_id FROM Groups WHERE name = '{}'"
                              .format(target_group)).fetchone()[0]
    update.effective_message.reply_text(
        text=asking_texts[group_id][lang(update)],
        reply_markup=ReplyKeyboardMarkup(
            [
                [BACK[lang(update)]]
            ],
            resize_keyboard=True)
    )
    payload = {
        update.effective_chat.id: group_id
    }
    context.chat_data.update(payload)
    return ASKING


def forward(update, context):
    message_id = update.effective_message.message_id
    chat_id = update.effective_message.chat_id
    group = context.chat_data[chat_id]
    msg = context.bot.forward_message(chat_id=group,
                                      from_chat_id=chat_id,
                                      message_id=message_id)
    user_info = cursor.execute("SELECT name, phone_number FROM Users WHERE telegram_id = '{}'"
                               .format(chat_id)).fetchmany()

    text = "Имя: {}\nТелефон: +{}"
    context.bot.send_message(chat_id=group,
                             text=text.format(user_info[0][0], user_info[0][1]))
    payload = {
        msg.message_id: chat_id
    }
    context.bot_data.update(payload)

    accept_request(update, context)
    return I_HAVE_A_QUESTION


def accept_request(update, context):
    chat_id = update.effective_chat.id
    update.effective_message.reply_text(
        gotcha_texts[context.chat_data[chat_id]][lang(update)]
    )
    ask_me_markup(update, context)


def reply_to_user(update, context):
    try:
        if update.message.reply_to_message:
            response = update.message.text
            reply_id = update.message.reply_to_message.message_id
            user_id = context.bot_data[reply_id]
            language = cursor.execute("SELECT language FROM Users WHERE telegram_id = '{}'"
                                      .format(user_id)).fetchone()[0]
            reply = txt_reply[language].format(response)
            context.bot.send_message(chat_id=user_id,
                                     text=reply,
                                     parse_mode='HTML')
        else:
            pass
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='На это ответить я не могу 😢\n'
                                      'Выберите реальный запрос который я вам отправил')
