from dotenv import load_dotenv
from os import environ as env
import telebot

load_dotenv()
try:
    TOKEN = env["TOKEN_BOT"]
    CHAT_ID= env["CHAT_ID"]
except KeyError:
    raise EnvironmentError(
        "Missing token"
    )

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['my_id'])
def id_print(message):
    bot.send_message(CHAT_ID, "asd")
    print("asd")

@bot.message_handler(commands=['change'])
def change(message):
    user = message.from_user.id
    promote(user, CHAT_ID)
    team_name = message.text.replace("/change ","")
    result = bot.set_chat_administrator_custom_title(CHAT_ID, user, team_name)
    print("change title:", result)


def promote(user, chat):
    result = bot.promote_chat_member(chat, user, can_change_info=True, can_invite_users=True)
    print("promote:", result)


bot.infinity_polling()

