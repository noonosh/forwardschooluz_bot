import time
from callbacks.static.texts import quiz_password_txt, text_quiz_instructions, quiz_finished_text, \
    quiz_thank_you
from constants import MAIN_MENU, TEST_PROCESS, TEST_READY_STATE
from user_settings import QUIZ_PASSWORD, QUIZ_RESULTS_CHANNEL_ID
from callbacks.mainpage import main_page
from databases.select import lang
from databases.database_connector import *
from telegram import (ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Poll,
                      ReplyKeyboardMarkup, ChatAction)
from telegram.ext import CallbackContext, ConversationHandler
from callbacks.static.button_texts import READY, SUBMIT_QUIZ_RESULTS
from callbacks.static.quiz_answers import *


def test_key(update, context):
    update.effective_message.reply_text(quiz_password_txt['request'][lang(update)],
                                        reply_markup=ReplyKeyboardRemove())
    return TEST_READY_STATE


def check_key(update, context):
    message = update.effective_message

    if message.text == QUIZ_PASSWORD:
        update.effective_message.reply_text(quiz_password_txt['confirm'][lang(update)])
        quiz_instructions(update, context)
        return ConversationHandler.END
    else:
        update.effective_message.reply_text(quiz_password_txt['reject'][lang(update)])
        main_page(update, context)
        return MAIN_MENU


def quiz_instructions(update, context):
    button = [
        [InlineKeyboardButton(READY[lang(update)], callback_data='start_that_quiz')]
    ]
    update.effective_message.reply_text(text_quiz_instructions[lang(update)],
                                        reply_markup=InlineKeyboardMarkup(button),
                                        parse_mode='HTML')


def quiz_getting_started(update, context):
    query = update.callback_query
    query.answer()
    query.message.delete()

    # Now it's time to save some data about this test

    payload = {
        'user': query.message.chat.id,
        'questions_answered': 0,
        'correct_answers': 0
    }
    context.user_data.update(payload)

    send_questions(update, context)
    # quiz_timer(update, context)
    return TEST_PROCESS


# def quiz_timer(update, context: CallbackContext):
#     context.job_queue.run_repeating(send_question, interval=31, first=0.1, context=context.user_data)


def check_poll_answer(update, context):
    if context.user_data[context.user_data['user']] == update.poll_answer.poll_id:

        if update.poll_answer.option_ids[0] == answers[context.user_data['questions_answered']]:
            context.user_data.update(
                {
                    'correct_answers': context.user_data['correct_answers'] + 1
                }
            )
        else:
            pass
        context.user_data.update(
            {
                context.user_data['questions_answered'] + 1
            }
        )
        send_questions(context, update)

    else:
        pass


def send_questions(update, context):
    if update.callback_query:
        n = str(1)

        """The very first question is sent from here."""
        msg = context.bot.send_poll(chat_id=update.effective_chat.id,
                                    question=questions[n].format(n),
                                    options=[
                                        options[n][0],
                                        options[n][1],
                                        options[n][2],
                                        options[n][3]
                                    ],
                                    type=Poll.QUIZ,
                                    correct_option_id=answers[n],
                                    is_anonymous=False)

        payload = {
            update.effective_chat.id: msg.poll.id
        }
        context.user_data.update(payload)
        print(context.user_data)

    elif update.poll_answer:

        if context.user_data[context.user_data['user']] == update.poll_answer.poll_id:

            if int(context.user_data['questions_answered'] + 1) < 50:

                current = context.user_data['questions_answered'] + 1
                next_queue = str(current + 1)

                # Add the answered question to the counter
                context.user_data.update(
                    {
                        'questions_answered': current
                    }
                )
                if str(update.poll_answer.option_ids[0]) == answers[str(current)]:
                    context.user_data.update(
                        {
                            'correct_answers': context.user_data['correct_answers'] + 1
                        }
                    )

                next_question = context.bot.send_poll(chat_id=context.user_data['user'],
                                                      question=questions[next_queue].format(next_queue),
                                                      options=[
                                                          options[next_queue][0],
                                                          options[next_queue][1],
                                                          options[next_queue][2],
                                                          options[next_queue][3]
                                                      ],
                                                      type=Poll.QUIZ,
                                                      correct_option_id=answers[next_queue],
                                                      is_anonymous=False)
                payload = {
                    context.user_data['user']: next_question.poll.id
                }

                context.user_data.update(payload)
            else:
                current = context.user_data['questions_answered'] + 1
                context.user_data.update(
                    {
                        'questions_answered': current
                    }
                )
                if str(update.poll_answer.option_ids[0]) == answers[str(current)]:
                    context.user_data.update(
                        {
                            'correct_answers': context.user_data['correct_answers'] + 1
                        }
                    )
                else:
                    pass
                close_quiz(update, context)
                return ConversationHandler.END
        else:
            pass


def close_quiz(update, context: CallbackContext):
    user = context.user_data['user']
    score = str(context.user_data['correct_answers'])
    language = cursor.execute("SELECT language FROM Users WHERE telegram_id = '{}'"
                              .format(user)).fetchone()[0]

    quiz_taker_name = cursor.execute("SELECT name FROM Users WHERE telegram_id = '{}'"
                                     .format(user)).fetchone()[0]
    quiz_taker_phone = '+' + cursor.execute("SELECT phone_number FROM Users WHERE telegram_id = '{}'"
                                            .format(user)).fetchone()[0]

    cursor.execute("""
    INSERT INTO QuizTakers (id, name, score) 
    VALUES ('{}', '{}', '{}')""".format(user, quiz_taker_name, score))
    conn.commit()

    markup = ReplyKeyboardMarkup(
        [
            [SUBMIT_QUIZ_RESULTS[language]]
        ],
        resize_keyboard=True
    )

    text = quiz_finished_text[language]
    results_text = "Name: {}\nPhone_number: {}\nScore: {}\nLevel: {}"

    if 0 < int(score) <= 15:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "BEGINNER"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'BEGINNER'))
    elif 16 <= int(score) <= 24:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "ELEMENTARY"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'ELEMENTARY'))
    elif 25 <= int(score) <= 32:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "PRE-INTERMEDIATE"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'PRE_INTERMEDIATE'))

    elif 33 <= int(score) <= 39:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "INTERMEDIATE"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'INTERMEDIATE'))
    elif 40 <= int(score) <= 45:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "UPPER INTERMEDIATE"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'UPPER INTERMEDIATE'))
    else:
        context.bot.send_chat_action(chat_id=user,
                                     action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=user,
                               photo=open("assets/images/quiz_finish.png", 'rb'),
                               caption=text.format(score, "ADVANCED"),
                               reply_markup=markup,
                               parse_mode='HTML')

        context.bot.send_message(chat_id=QUIZ_RESULTS_CHANNEL_ID,
                                 text=results_text.format(quiz_taker_name,
                                                          quiz_taker_phone,
                                                          score,
                                                          'ADVANCED'))


def completed_quiz(update, context: CallbackContext):
    update.effective_message.reply_text(quiz_thank_you[lang(update)],
                                        reply_markup=ReplyKeyboardRemove())
    time.sleep(0.3)
    main_page(update, context)
    return MAIN_MENU
