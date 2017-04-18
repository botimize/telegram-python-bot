import apiai
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from botimize import Botimize

# Declare updater & dispatcher
my_token = '355205992:AAHYySfOCKFxuNFPr2b_y-JbaxTW7eRCZRQ'
updater = Updater(token=my_token)
dispatcher = updater.dispatcher

# Declare APIAI
CLIENT_ACCESS_TOKEN = 'eaa4f162d7144c3ca2b04c9dd829a61d'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# Declare Botimize
botimize = Botimize('I472Y6HIBBE51UMDZFHXI0EATOVQPLH9', 'facebook') # temporary use facebook platfrom

# Customize function
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def resp(bot, update):
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = update.message.chat_id
    request.query = update.message.text
    response = request.getresponse().read().decode("utf-8")
    responseText = json.loads(response)["result"]["fulfillment"]["speech"]
    bot.sendMessage(chat_id=update.message.chat_id, text=responseText)
    # botimize incoming
    data_in = {}
    data_in['entry']=[{}]
    data_in['entry'][0]['messaging']=[{}]
    data_in['entry'][0]['messaging'][0]['sender'] = {'id': update.message.chat_id}
    data_in['entry'][0]['messaging'][0]['message'] = {'text': update.message.text} 
    botimize.log_incoming(data_in)
    # botimize outgoing
    data_out = {
        "recipient": { "id": update.message.chat_id},
        "message": { "text": responseText}
    }
    botimize.log_outgoing(data_out)

# Structuralize bot (custom functions -> dispatcher)
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, resp)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Update to telegram platfrom
updater.start_polling()
updater.idle()

