import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)

from digitalize_bot import config, handlers


if not config.BOT_TOKEN:# or not config.BOT_CHANNEL_ID:
    raise ValueError(
        'BOT_TOKEN or BOT_CHANNEL_ID env variables'
        'was not provided in .env (both should be initialized)'
    )

COMMAND_HANDLERS = {
    'start': handlers.start,
    'help': handlers.help_,
    'all_books': handlers.all_books,
    'create_book': handlers.create_book,
    'create_category': handlers.create_category,
    'my_books': handlers.my_books
}

CALLBACK_QUERY_HANDLERS = {
    rf'^{config.ALL_BOOKS_CALLBACK_PATTERN}(\d+)$': handlers.all_books_buttons,
    # rf'^{config.VOTE_BOOKS_CALLBACK_PATTERN}(\d+)$': handlers.vote_button
}

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)


def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, command_handler))

    for pattern, handler in CALLBACK_QUERY_HANDLERS.items():
        app.add_handler(CallbackQueryHandler(handler, pattern=pattern))

    app.add_handler(MessageHandler(filters.Regex(r'^/b\d+$'), handlers.handle_borrow_number))
    app.add_handler(MessageHandler(filters.Regex(r'^/r\d+$'), handlers.handle_return_number))

    app.add_handler(handlers.conv_handler)
    app.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback

        # logger.warning(traceback.format_exc())