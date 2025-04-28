import telebot
from dotenv import load_dotenv
from telebot import types
from pathlib import Path
from os import getenv


dotenv_path = Path('/ToolSuggestionBot/.env')
load_dotenv(dotenv_path=dotenv_path)
bot = telebot.TeleBot(getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    bot.send_message(message.from_user.id, "👋Hi, I'm a ToolSuggestionBot. I can help you with choosing a tool"
                                           "for your needs. Type /help to see the list of my commands.")


@bot.message_handler(commands=['help'])
def handle_help(message: types.Message):
    bot.send_message(message.from_user.id, parse_mode='MarkdownV2', text="Here's the list of all my commands:\n"
                                            "***/help***: Prints this message\.\n"
                                            "***/start***: Prints welcome message\.\n")

bot.infinity_polling()