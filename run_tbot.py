"""Fix's imports"""
from telegram import Update  # ForceReply
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler

import utils
import chatgpt
from keys import telegram_api_key
from cache import BotCacheClient


async def hi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hi_text = 'Вы можете у меня спросить практически о чем угодно: ' \
        'о фактах, истории, математике, языках, путешествиях, технике, спорте и т.д. ' \
        'Я постараюсь помочь вам с информацией или ответить на вопрос.'
    await update.message.reply_text(hi_text)


async def get_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keys = update.effective_message.text.split(' ')
    keys.remove('/key')
    keys_count = len(keys)
    keys = [key for key in keys if len(key) == 51 and key.startswith('sk-')]
    valid_keys_count = len(keys)
    await update.message.reply_text(f'Всего ключей: {keys_count}. Из них валидных добавлено: {valid_keys_count}.')


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cart = '5375 4141 3166 6256 - Monobank\n' \
        'Укажите в коммент. оплаты свой телеграм!\n' \
        'Подписка на неделю: 100 UAH.\n' \
        'Подписка на месяц: 300 UAH.\n' \
        '50% с дохода будет перечислено на ВСУ !!!'
    await update.message.reply_text(cart)


async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = '/key ключ1 ключ2 - передать api-ключи для бота. (Можно несколько разделив пробелом)\n' \
        '/msg сообщение - сообщение для разработчика.'
    await update.message.reply_text(help_text)


async def message_to_developer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    message = update.effective_message.text.split(' ')
    message.remove('/msg')
    message = ' '.join(message)
    text = f'Сообщение от @{user_name} id:{user_id} - {message}'
    if len(message) != 0:
        await context.bot.send_message(chat_id=414902937, text=text)
        await update.message.reply_text('Сообщения доставлены разработчику.')
    else:
        await update.message.reply_text('Введите сообщение после команды.')


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    The main function of processing clients messages
    """
    acache = BotCacheClient("127.0.0.1", 11211)

    user_id = update.effective_user.id
    user_name = update.effective_user.username
    user_message = update.effective_message.text

    history = await acache.get_or_create_history(user_id)
    history.append({'role': 'user', 'content': user_message})
    system_answer = await chatgpt.get_answer(list(history))
    history.append({'role': 'system', 'content': system_answer})
    await acache.update_history(user_id, history)

    await update.message.reply_text(system_answer)
    utils.logging(f'FiX ответил пользователю - @{user_name} id:{user_id} на сообщение, - \"{user_message}\".')

    await acache.close()


def main() -> None:
    """
    Run the fix-bot
    """
    utils.logging('Fix Запущен.')
    application = Application.builder().token(telegram_api_key).build()
    application.add_handler(CommandHandler('start', hi))
    application.add_handler(CommandHandler('help', show_commands))
    application.add_handler(CommandHandler('msg', message_to_developer))
    application.add_handler(CommandHandler('pay', show_cart))
    # application.add_handler(CommandHandler('key', get_key))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    finally:
        utils.logging('Fix Завершает работу.')
