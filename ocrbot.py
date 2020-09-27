try:
    from PIL import Image
except ImportError:
    import Image
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import Update, Bot, ParseMode
import os
import pytesseract

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \n\nWelcome to ocr bot.\n send me a image  ' )


def search(bot, update):
    """Send reply of user's message."""
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('testing.jpg')
    try:
        output=pytesseract.image_to_string(Image.open('testing.jpg'))
        update.message.reply_text('`'+str(output)+'`',parse_mode=ParseMode.MARKDOWN,reply_to_message_id=update.message.message_id)
    except Exception as e:
        update.message.reply_text(e)
        try:
            os.remove('testing.jpg')
        except Exception:
            pass

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    #ocr_bot_token="your token then comment below line"
    
    ocr_bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(ocr_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, search))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
