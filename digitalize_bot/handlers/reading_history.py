from telegram import Update
from telegram.ext import ContextTypes

from digitalize_bot.db import async_session_maker
from digitalize_bot.handlers.response import send_response
from digitalize_bot.crud.book_crud import book
from digitalize_bot.crud.users_books_crud import users_books
from digitalize_bot.crud.user_crud import user
from digitalize_bot.templates import render_template


async def reading_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = async_session_maker()
    user_id = update.effective_user.id

    history = await users_books.get_history(session, user_id)
    existing_user = await user.get_by_id(session, user_id)

    if not existing_user:
        await update.message.reply_text('Вы не зарегистрированы, пожалуйста /register')
        return

    if not update.message:
        return

    if history:
        await send_response(
        update,
        context,
        render_template('history.j2', {'history': history})
    )
    else:
        await update.message.reply_text('Вы ещё не читали книги, /all_books.')





