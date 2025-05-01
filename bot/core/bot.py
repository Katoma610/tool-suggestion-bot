import telebot
from dotenv import load_dotenv
from telebot import types
from pathlib import Path
from os import getenv
from ..utils.toolparsing import ToolParsing, format_tools
from functools import reduce


dotenv_path = Path('/ToolSuggestionBot/.env')
load_dotenv(dotenv_path=dotenv_path)
bot = telebot.TeleBot(getenv('BOT_TOKEN'))

tools = ToolParsing('bot/data/tools.json')
categories = tools.get_categories()
category_buttons = [types.InlineKeyboardButton(category, callback_data=category) for category in categories]
category_markup = types.InlineKeyboardMarkup(row_width=2)
category_markup.add(*category_buttons)
all_subcategories = reduce(lambda a, b: a+b, [tools.get_subcategories(category) for category in categories])
curr_category = 'None'

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    bot.send_message(message.from_user.id, "👋Hi, I'm a ToolSuggestionBot. I can help you with choosing a tool"
                                           "for your needs. Type /help to see the list of my commands.")


@bot.message_handler(commands=['help'])
def handle_help(message: types.Message):
    bot.send_message(message.from_user.id, parse_mode='MarkdownV2', text="Here's the list of all my commands:\n"
                                            "***/help***: Prints this message\.\n"
                                            "***/start***: Prints welcome message\.\n"
                                            "***/categories***: Opens categories menu\.")


@bot.message_handler(commands=['categories'])
def handle_categories(message: types.Message):
    bot.send_message(message.from_user.id, reply_markup=category_markup, text="Choose a category from below:")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: types.CallbackQuery):
    prev_message = call.message
    if call.data in categories:
        global curr_category
        curr_category = call.data
        subcategory_buttons = [types.InlineKeyboardButton(subcategory, callback_data=subcategory)
                               for subcategory in tools.get_subcategories(call.data)]
        subcategory_markup = (types.InlineKeyboardMarkup(row_width=2)
                              .add(*subcategory_buttons)
                              .add(types.InlineKeyboardButton('See all', callback_data='See all'))
                              .add(types.InlineKeyboardButton(' << Back to categories', callback_data='Back to categories')))
        bot.edit_message_text(f"Choose a subcategory from below or press See all to see all tools of chosen category({call.data}):",
                              message_id=prev_message.id, chat_id=prev_message.chat.id,
                              reply_markup=subcategory_markup)
    elif call.data in tools.get_subcategories(curr_category):
        tool_text = format_tools(tools.get_tools(curr_category, call.data))
        bot.edit_message_text(f"Tools for {curr_category}, {call.data}:\n\n{tool_text}",
                              message_id=prev_message.id, chat_id=prev_message.chat.id)
    elif call.data == 'See all':
        tool_text = '\n\n'.join(format_tools(tools.get_tools(curr_category, sub)) for sub in tools.get_subcategories(curr_category))
        bot.edit_message_text(f"All tools for {curr_category}:\n\n{tool_text}",
                              message_id=prev_message.id, chat_id=prev_message.chat.id)
    elif call.data == 'Back to categories':
        bot.edit_message_text("Choose a category from below:", message_id=prev_message.id,
                              chat_id=prev_message.chat.id, reply_markup=category_markup)


bot.infinity_polling()