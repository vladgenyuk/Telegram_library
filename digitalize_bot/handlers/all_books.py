import telegram

from telegram import Update
from telegram.ext import ContextTypes

from digitalize_bot import config
from digitalize_bot.db import async_session_maker
from digitalize_bot.handlers.keyboard import get_categories_keyboard
from digitalize_bot.handlers.response import send_response

from digitalize_bot.crud.book_crud import book
from digitalize_bot.models.books import Book
from digitalize_bot.templates import render_template


def _get_category_index(query_data) -> int:
    pattern_prefix_length = len(config.ALL_BOOKS_CALLBACK_PATTERN)
    return int(query_data[pattern_prefix_length:])


def group_by_categories(books: list[Book]) -> dict:
    hashset = {}
    for book in books:
        if not hashset.get(book.category_title):
            hashset[book.category_title] = [book]
            continue
        hashset[book.category_title].append(book)
    return hashset


async def all_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = async_session_maker()
    books = await book.get_all_books(session)
    categories_with_books = group_by_categories(books)

    if not update.message:
        return

    current_category = list(categories_with_books.keys())[0]

    await send_response(
        update,
        context,
        render_template(
            'all_books.j2',
            {
                'category': current_category,
                'start_index': None,
                'books': categories_with_books[current_category],
            }
        ),
        get_categories_keyboard(
            current_category_index=0,
            categories_count=len(categories_with_books),
            callback_prefix=config.ALL_BOOKS_CALLBACK_PATTERN
        )
    )


async def all_books_buttons(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not query.data or not query.data.strip():
        return

    session = async_session_maker()
    books = await book.get_all_books(session)
    categories_with_books = group_by_categories(books)
    current_category_index = _get_category_index(query.data)

    current_category = list(categories_with_books.keys())[current_category_index]

    await query.edit_message_text(
        text=render_template(
            'all_books.j2',
            {
                'category': current_category,
                'start_index': None,
                'books': categories_with_books[current_category],
            },
        ),
        reply_markup=get_categories_keyboard(
            current_category_index=current_category_index,
            categories_count=len(categories_with_books),
            callback_prefix=config.ALL_BOOKS_CALLBACK_PATTERN
        ),
        parse_mode=telegram.constants.ParseMode.HTML
    )
