from user_settings import VIDEO_1_ID, VIDEO_2_ID, VIDEO_3_ID
from databases.select import lang
from user_settings import ADMIN_IDS
from callbacks.mainpage import back_to_main
from callbacks.static.texts import video_1_caption, video_2_caption, video_3_caption


def video_1(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_video(chat_id=telegram_id,
                           video=VIDEO_1_ID,
                           caption=video_1_caption[lang(update)])


def video_2(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_video(chat_id=telegram_id,
                           video=VIDEO_2_ID,
                           caption=video_2_caption[lang(update)])


def video_3(update, context):
    telegram_id = update.message.chat_id
    context.bot.send_video(chat_id=telegram_id,
                           video=VIDEO_3_ID,
                           caption=video_3_caption[lang(update)])


def get_video_id(update, context):
    telegram_id = update.message.chat_id
    if telegram_id in ADMIN_IDS:
        context.bot.send_message(chat_id=telegram_id,
                                 text=update.message.video.file_id)
    else:
        back_to_main(update, context)
