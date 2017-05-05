import apiai
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from botimize1 import Botimize

# Declare updater & dispatcher 
telegram_token = '355205992:AAHYySfOCKFxuNFPr2b_y-JbaxTW7eRCZRQ'
updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher

# Declare Botimize
botimize_apiKey = 'I472Y6HIBBE51UMDZFHXI0EATOVQPLH9'
botimize = Botimize(botimize_apiKey, 'generic')

# Customize function
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def resp(bot, update):
    echo_response = update.message.text
    bot.sendMessage(chat_id=update.message.chat_id, text=echo_response)
    
    # botimize incoming
    incomingLog = {
        'sender': {
          'id': update.message.chat_id,
          'name': 'USER_SCREEN_NAME'
        },
        'content': {
            'type': 'text', 
            'text':  echo_response
        }
    }
    botimize.log_incoming(incomingLog)
    # botimize outgoing
    outgoingLog = {
        'receiver': {
          'id': update.message.chat_id,
          'name': 'USER_SCREEN_NAME'
        },
        'content': {
            'type': 'text',
            'text': echo_response
        }
    }
    print(botimize.log_outgoing(outgoingLog))

# Structuralize bot (custom functions -> dispatcher)
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, resp)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Update to telegram platfrom
updater.start_polling()
updater.idle()

