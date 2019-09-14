import telegram
from telegram.ext import Updater, CommandHandler
from functools import wraps
import asyncio
import logging
import safetoken
from birthday import birthdaylist
key = safetoken.apikey
updater = Updater(token=key, use_context=True)
dp = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
from datetime import datetime, timedelta, date,time
birthdays = birthdaylist
wish = 0


def send_typing_action(func):
    @wraps(func)
    def command_func(update,context,*args,**kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context, *args, *kwargs)
    return command_func


def get_until_tomorrow():
    now = datetime.now()
    today = date.today()
    tomorrow_date = today + timedelta(days=1)
    tomorrow = datetime.combine(tomorrow_date,time=time(00,00))
    seconds_left = tomorrow - now
    return seconds_left.seconds


async def wish_tomorrow(update, context):
    global wish
    await asyncio.sleep(get_until_tomorrow())
    print("!", wish)
    wish = 0
    print(wish)
    wish_people(update, context)


@send_typing_action
def wish_people(update, context):
    global wish
    today = date.today().strftime("%d-%m")
    if wish == 0:
        if today in birthdays:
            context.bot.send_message(chat_id=update.message.chat_id, text="Happy Birthday {} !!! ".format(birthdays[today]["username"]))
            wish = 1
    else:
        wish_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(wish_loop)
        wish_loop.run_until_complete(wish_tomorrow(update, context))


async def main():
    dp.add_handler(CommandHandler("start_wishing", wish_people))
    updater.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
