# import asyncio
from telegram import Update  # ForceReply
from telegram.ext import Application, ContextTypes, MessageHandler, filters  # CommandHandler
from cache import cache
from utils import key_generator, logging
import openai
import openai.error


# Api ChatGPT
chatgpt_keys = [
    None  # Keys
]
key = key_generator(chatgpt_keys)
openai.api_key = next(key)
# Api Telegram
fix_api_key = None  # Keys


async def get_answer(history: list):
    answer = await openai.ChatCompletion.acreate(
        model='gpt-3.5-turbo',
        messages=history,
    )
    return answer['choices'][0]['message']['content']


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        user_message = update.effective_message.text
        history = await cache.get_or_create_history(user_id, 25, 300)
        history.append({'role': 'user', 'content': user_message})
        system_answer = await get_answer(list(history))
        history.append({'role': 'system', 'content': system_answer})
        await cache.update_history(user_id, history, 300)

        await update.message.reply_text(system_answer)
        logging(f'FiX ответил пользователю - @{user_name} id:{user_id} на сообщение, - \"{user_message}\".')

    except openai.error.ServiceUnavailableError:
        await update.message.reply_text('Сервер перегружен. Попробуйте ещё раз.')
        logging(f'FiX НЕ ответил пользователю - @{user_name} id:{user_id} на сообщение, - \"{user_message}\"')

    except openai.error.RateLimitError:
        openai.api_key = next(key)
        logging('Fix сменил Api-ключ и идет на повторный ответ.')
        await handler(update, context)


def fix_run() -> None:
    logging('Fix Запущен.')
    application = Application.builder().token(fix_api_key).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        fix_run()
    except RuntimeError:
        pass
    except KeyboardInterrupt:
        exit()
    finally:
        logging('Fix Завершает работу.')  # {get_db_size(cache)}
