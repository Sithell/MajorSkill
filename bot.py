from engine import Engine
from telebot import TeleBot, types

token = '396661224:AAEhmcS8sfEL7dq9892WNUOWTWWGCyfNKDw'
bot = TeleBot(token)
loading = open('loading.gif', 'rb')

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
    bot.send_document(message.chat.id, loading)
    print(message.text)
    engine = Engine()
    result = engine.parser(message.text)
    print(result)
    print()

    for item in result:  # pretty print
        percent = str(round(item[1] * 100)) + '%'
        course = engine.get_item('course', param='name', value=item[0])[0]
        answer = item[0] + ' - ' + percent + '\n' + course

        bot.send_message(message.chat.id, answer)

    del engine

if __name__ == '__main__':
    bot.polling(none_stop=True)
