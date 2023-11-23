from telegram import Update
from telegram.ext import CallbackContext

from digitalize_bot.db import async_session_maker
from digitalize_bot.models.users import user
from digitalize_bot.models.users_books import users_books


async def handle_borrow_number(update: Update, context: CallbackContext) -> None:
    session = async_session_maker()
    number = int(update.message.text[2:])

    user_id = update.effective_user.id
    existing_user = await user.get_user_by_id(session, user_id)

    if not existing_user:
        await update.message.reply_text('Вы не зарегистрированы, пожалуйста /register')
        return

    users_books_data = {
        'book_id': number,
        'user_id': update.effective_user.id
    }
    await users_books.create_users_books(session, users_books_data)

