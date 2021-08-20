import flask
import telebot
import words
from dotenv import load_dotenv


load_dotenv()
app = flask.Flask(__name__)
bot = telebot.TeleBot(environ.get("TG_TOKEN"), threaded=False)
WEBHOOK_URL_PATH = "/%s/" % (environ.get("TG_TOKEN"))

# # Remove webhook, it fails sometimes the set if there is a previous webhook
# bot.remove_webhook()
# time.sleep(1)
# # Set webhook
# bot.set_webhook(url=environ.get("WEBHOOK_URL") + WEBHOOK_URL_PATH)


@bot.message_handler(commands=['ping'])
def ping(message):
    return bot.reply_to(message, "pong")


@bot.message_handler(commands=['start_game'])
def start_game(message):
    if "group" in message.chat.type:
        admins = bot.get_chat_administrators(message.chat.id)
        w = words.Words()
        for a in admins:
            if message.from_user.id == a.user.id:
                return bot.reply_to(message, w.start_game())
    return bot.reply_to(message, "Only admins can do that!")


@bot.message_handler(commands=['ranks'])
def ranks(message):
    w = words.Words()
    return bot.reply_to(message, "`" + w.rankings() + "`", parse_mode="Markdown")


@bot.message_handler(commands=['ans'])
def answer(message):
    if message.chat.id == message.from_user.id:
        return bot.reply_to(message, "Sorry, its command work only on public chats.")
    w = words.Words()
    ans = message.text.split(' ')
    if len(ans) == 2:
        return bot.reply_to(message, w.check(message.from_user.first_name, ans[1]))
    return bot.reply_to(message, "Wrong command. You should use /ans <pkm_name>")
