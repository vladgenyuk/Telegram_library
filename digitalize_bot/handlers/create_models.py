from telegram import Update
from telegram.ext import ContextTypes

from digitalize_bot.handlers.response import send_response
from digitalize_bot.templates import render_template
from digitalize_bot.crud.book_crud import book
from digitalize_bot.crud.category_crud import category
from digitalize_bot.db import async_session_maker


async def create_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = async_session_maker()
    await book.create(session, {
        'title': 'book2',
        'position_number': 1,
        'category_id': 4,
    })
    await send_response(update, context, response=render_template('create.j2', data={'model': 'book'}))


async def create_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = async_session_maker()
    await category.create(session, {
        'title': "Title2"
    })
    await send_response(update, context, response=render_template('create.j2', data={'model': 'category'}))
