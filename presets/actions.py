from functools import wraps


def send_action(action):
    """Sends 'action' while processing func command"""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                         action=action)
            return command_func(update, context, *args, **kwargs)

        return decorator
