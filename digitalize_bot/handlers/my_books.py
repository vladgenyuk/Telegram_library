from telegram import Update
from telegram.ext import ContextTypes

from digitalize_bot.db import async_session_maker
from digitalize_bot.handlers.response import send_response
from digitalize_bot.crud.book_crud import book
from digitalize_bot.crud.user_crud import user
from digitalize_bot.templates import render_template


async def my_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = async_session_maker()
    user_id = update.effective_user.id
    existing_user = await user.get_by_id(session, user_id)

    if not existing_user:
        await update.message.reply_text('Вы не зарегистрированы, пожалуйста /register')
        return

    books = await book.get_my_books(session, user_id)

    if not update.message:
        return

    if books:
        await send_response(
        update,
        context,
        render_template('my_books.j2', {'books': books})
    )
    else:
        await update.message.reply_text('У вас ещё нет книг, /all_books.')



