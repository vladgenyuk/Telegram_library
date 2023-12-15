import datetime

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler,\
    CommandHandler, MessageHandler, filters

from sqlalchemy.exc import IntegrityError

from digitalize_bot.db import async_session_maker
from digitalize_bot.crud.user_crud import user


FIRST_NAME, LAST_NAME, EMAIL = range(3)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['/cancel']]

    await update.message.reply_text(
        text='Введите ваше имя (first_name) или /cancel.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    # await send_response()
    return FIRST_NAME


async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['first_name'] = update.message.text

    await update.message.reply_text('Введите вашу фамилию.')

    return LAST_NAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['last_name'] = update.message.text

    await update.message.reply_text('Введите ваш email.')

    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text

    session = async_session_maker()
    context.user_data['id'] = update.effective_user.id
    context.user_data['registered_at'] = datetime.datetime.now()
    try:
        await user.create_user(session, context.user_data)
    except ValueError as e:
        await update.message.reply_text("Введите корректный email например user@example.com")
        return EMAIL
    except IntegrityError as e:
        await update.message.reply_text('Пользователь с таким user_id уже зарегистрирован или данная почта уже есть в нашей базе данных')
        return ConversationHandler.END

    await update.message.reply_text('Спасибо, ваша информация сохранена.')
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text('Регистрация завершена.')

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('register', register)],
    states={
        FIRST_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), first_name)],
        LAST_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), last_name)],
        EMAIL: [MessageHandler(filters.TEXT & (~filters.COMMAND), email)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
