import telebot
import random

from telebot import types

bot = telebot.TeleBot("5099555428:AAExGdnW8mnRAAFD-wBzt4KmDSViD8jsIMs")

data_consts = dict()
data_ids = set()


@bot.message_handler(commands=['start'])
def starting(message):
    img = open('static/club.jpeg', 'rb')
    bot.send_photo(message.chat.id, img)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("Задать диапозон")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     f"Ку, {message.from_user.first_name}!\nЭто бот простой бот для рандома чисел в диапозоне.",
                     parse_mode='html', reply_markup=markup)


def fill_markup_random(markup):
    item1 = types.InlineKeyboardButton("Задать левую границу", callback_data='left')
    item2 = types.InlineKeyboardButton("Задать правую границу", callback_data='right')
    item3 = types.InlineKeyboardButton("Зарандомить", callback_data='lets_go')

    markup.add(item1, item2, item3)


def is_number(text):
    if text.isnumeric():
        return True

    if len(text) > 1 and text[0] == '-' and text[1:].isnumeric():
        return True

    return False


def print_random(chat_id):
    data_consts[chat_id][2] = "none"
    if data_consts[chat_id][0] > data_consts[chat_id][1]:
        img = open('static/pasha.jpeg', 'rb')
        bot.send_photo(chat_id, img)
        bot.send_message(chat_id, "Ты мне кажется что-то перепутал...")
    else:
        answer = random.randint(data_consts[chat_id][0], data_consts[chat_id][1])
        bot.send_message(chat_id, f"Рандомим из диапозона: ({data_consts[chat_id][0]};"
                                  f"{data_consts[chat_id][1]})\nДело сделано: {answer}!")


@bot.message_handler(content_types=['text'])
def simple_text(message):
    if message.chat.id not in data_ids:
        data_consts[message.chat.id] = [0, 100, "none"]
        data_ids.add(message.chat.id)

    if message.text == '🎲 Рандомное число':
        print_random(message.chat.id)
    elif message.text == 'Задать диапозон':
        markup = types.InlineKeyboardMarkup(row_width=3)
        fill_markup_random(markup)

        bot.send_message(message.chat.id, f"оооооокей летс гоу\nТекущие границы: ({data_consts[message.chat.id][0]};"
                                          f"{data_consts[message.chat.id][1]})",
                         reply_markup=markup)
    elif is_number(message.text):
        if data_consts[message.chat.id][2] == "none":
            bot.send_message(message.chat.id, 'И зачем мне это число?')
        else:

            if data_consts[message.chat.id][2] == 'left':
                data_consts[message.chat.id][0] = int(message.text)
            elif data_consts[message.chat.id][2] == 'right':
                data_consts[message.chat.id][1] = int(message.text)
            data_consts[message.chat.id][2] = "none"

            markup = types.InlineKeyboardMarkup(row_width=3)
            fill_markup_random(markup)

            bot.send_message(message.chat.id,
                             f"Текущие границы: ({data_consts[message.chat.id][0]};"
                             f"{data_consts[message.chat.id][1]})",
                             reply_markup=markup)
    else:
        if data_consts[message.chat.id][2] != "none":
            bot.send_message(message.chat.id, 'Ты что число написать не можешь?')
        elif message.text == 'hello':
            stik = open('static/hello.webp', 'rb')
            bot.send_sticker(message.chat.id, stik)
        else:
            bot.send_message(message.chat.id, 'Больше я пока ничего не могу, не пиши сюда.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'left':
                data_consts[call.message.chat.id][2] = "left"
                bot.send_message(call.message.chat.id, 'Введи левую границу')
            elif call.data == 'right':
                data_consts[call.message.chat.id][2] = "right"
                bot.send_message(call.message.chat.id, 'Введи правую границу')
            else:
                print_random(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="🎲 Рандомное число из диапозона",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
