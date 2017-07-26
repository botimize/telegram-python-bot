import apiai
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from botimize import Botimize

# Declare updater & dispatcher 
telegram_bot_token = 'Your_Telegram_Token'
updater = Updater(token=telegram_bot_token)
dispatcher = updater.dispatcher

# Declare Botimize
botimize_apiKey = 'Your_Botimize_Api_Key'
botimize = Botimize(botimize_apiKey, 'telegram', {
    'apiUrl': 'https://api.getbotimize.com',
})

# Customize function
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def resp(bot, update):
    echo_response = update.message.text
    bot.sendMessage(chat_id=update.message.chat.id, text=echo_response)
    # botimize incoming
    botimize.log_incoming(update.to_dict())
    # botimize outgoing
    outgoingLog = {
        'token': telegram_bot_token,
        'chat_id': update.message.chat.id,
        'text': echo_response
    }
    botimize.log_outgoing(outgoingLog)

# Structuralize bot (custom functions -> dispatcher)
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, resp)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Update to telegram platfrom
updater.start_polling()
updater.idle()
