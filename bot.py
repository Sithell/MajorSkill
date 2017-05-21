from engine import Engine
from telebot import TeleBot, types
# import threading
# import time

token = '396661224:AAEhmcS8sfEL7dq9892WNUOWTWWGCyfNKDw'
bot = TeleBot(token)


@bot.message_handler(commands=["start", "info"])
def info(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("Web-разработчик")
    btn2 = types.KeyboardButton("Android developer")
    btn3 = types.KeyboardButton("Программист Unity")
    btn4 = types.KeyboardButton("Web-дизайнер")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Введите название специальности или выберите из списка:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def message_handler(message):
    # threading.Timer(0, play_animation, args=[message.chat.id]).start()
    print("message received: chat id {0}, message id {1}".format(message.chat.id, message.message_id))
    bot.send_message(message.chat.id, "Подождите...")

    engine = Engine()
    result = engine.parser(message.text)

    for item in result:  # pretty print
        percent = str(round(item[1] * 100)) + '%'
        course = engine.get_item('course', param='name', value=item[0])[0]
        answer = item[0] + ' - ' + percent + '\n' + course

        bot.send_message(message.chat.id, answer)

    del engine


# def play_animation(chat_id):
#     global event
#     message_id = bot.send_message(chat_id, "Подождите...").message_id
#     time.sleep(0.25)
#
#     while not event.is_set():
#         bot.edit_message_text("Подождите", chat_id, message_id)
#         time.sleep(0.25)
#         bot.edit_message_text("Подождите.", chat_id, message_id)
#         time.sleep(0.25)
#         bot.edit_message_text("Подождите..", chat_id, message_id)
#         time.sleep(0.25)
#         bot.edit_message_text("Подождите...", chat_id, message_id)
#         time.sleep(0.25)
#
#     bot.edit_message_text("Готово!", chat_id, message_id)
#     event.clear()


if __name__ == '__main__':
    bot.polling(none_stop=True)
