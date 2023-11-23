from telegram import Update
from telegram.ext import ContextTypes

from digitalize_bot.handlers.response import send_response
from digitalize_bot.templates import render_template


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, response=render_template('help.j2'))