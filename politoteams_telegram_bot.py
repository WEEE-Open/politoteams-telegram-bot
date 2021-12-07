from dotenv import load_dotenv
from os import environ as env
import telebot
import team_list

load_dotenv()
try:
    TOKEN = env["TOKEN_BOT"]
    CHAT_ID = env["CHAT_ID"]
except KeyError:
    raise EnvironmentError(
        "Missing token"
    )

bot = telebot.TeleBot(TOKEN)
prev_message = ''


@bot.message_handler(commands=['chat_id'])
def get_chat_id(message):
    chat = message.chat.id
    print(chat)


@bot.message_handler(commands=['test'])
def id_print(message):
    user = message.from_user
    username = user.username
    bot.send_message(CHAT_ID, username+" says asd")


@bot.message_handler(commands=['change'])
def change(message):
    user = message.from_user
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    names = team_list.names
    itembtn1 = telebot.types.KeyboardButton(names[0])
    itembtn2 = telebot.types.KeyboardButton(names[1])
    itembtn3 = telebot.types.KeyboardButton(names[2])
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Choose the team", reply_markup=markup)
    promote(user.id, CHAT_ID)
    global prev_message
    prev_message = message
    '''team_name = message.text.replace("/change ","")
    result = bot.set_chat_administrator_custom_title(CHAT_ID, user.id, team_name)
    bot.send_message(CHAT_ID, user.username + " changes title to " + team_name)
    print("change title:", result)'''


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Welcome, use /change to change you title in group chat")


@bot.message_handler(func=lambda message: True)
def check_message(message):
    global prev_message
    if prev_message.text == '/change':
        change_title(message)
    prev_message = message


def change_title(message):
    user = message.from_user
    result = bot.set_chat_administrator_custom_title(CHAT_ID, user.id, message.text)
    print("change title: ", result)
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Changed title to "+message.text, reply_markup=markup)


def promote(user, chat):
    result = bot.promote_chat_member(chat, user, can_change_info=True, can_invite_users=True)
    print("promote:", result)


bot.infinity_polling()

