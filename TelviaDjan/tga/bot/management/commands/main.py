from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.utils.request import Request

from bot.models import Profile
from bot.models import Message

TOKEN = '1286048999:AAHn2LtAN5C5VjGvMo5WEi_dPqzoRmos1Jc'


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:

            error_message = f'Error: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    Message(
        profile=p,
        text=text
    ).save()

    reply_text = f'Hi, id - {chat_id}, txt = {p.name}'
    update.message.reply_text(
        text=reply_text,
    )


class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True
        )

        message_handler = MessageHandler(
            Filters.text, do_echo
        )
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
