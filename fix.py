"""Fix's imports"""
import openai
import openai.error
from telegram import Update  # ForceReply
from telegram.ext import Application, ContextTypes, MessageHandler, filters  # CommandHandler

from . import utils
from .keys import openai_api_keys, telegram_api_key
from .cache import FixClient
# import asyncio


# Api ChatGPT
chatgpt_keys = openai_api_keys
key = utils.key_generator(chatgpt_keys)
openai.api_key = next(key)
# Api Telegram
FIX_API_KEY = telegram_api_key
# Cache settings
LENGHT_OF_DATA = 15
TIME_OF_EXP = 60 * 30  # seconds


async def get_answer(history: list):
    """
    This method does a request to ChatGPT
    """
    answer = await openai.ChatCompletion.acreate(
        model='gpt-3.5-turbo',
        messages=history,
    )
    return answer['choices'][0]['message']['content']


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The main function of processing clients messages
    """
    try:
        acache = FixClient("127.0.0.1", 11211)
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        user_message = update.effective_message.text
        history = await acache.get_or_create_history(user_id, LENGHT_OF_DATA, TIME_OF_EXP)
        history.append({'role': 'user', 'content': user_message})
        system_answer = await get_answer(list(history))
        history.append({'role': 'system', 'content': system_answer})
        await acache.update_history(user_id, history, TIME_OF_EXP)

        await update.message.reply_text(system_answer)
        utils.logging(f'FiX ответил пользователю - @{user_name} id:{user_id} на сообщение, - \"{user_message}\".')

    except openai.error.RateLimitError:
        openai.api_key = next(key)
        utils.logging('Fix сменил Api-ключ и идет на повторный ответ.')
        await handler(update, context)

    except openai.error.ServiceUnavailableError:
        await update.message.reply_text('Сервер OpenAi перегружен. Попробуйте ещё раз.')
        utils.logging(f'FiX НЕ ответил пользователю - @{user_name} id:{user_id} на сообщение, - \"{user_message}\"')

    finally:
        await acache.close()


def fix_run() -> None:
    """
    Run the fix-bot
    """
    utils.logging('Fix Запущен.')
    application = Application.builder().token(FIX_API_KEY).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        fix_run()
    finally:
        utils.logging('Fix Завершает работу.')
