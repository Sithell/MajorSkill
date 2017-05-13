from engine import Engine
import telebot

token = '339228067:AAGSfEToYqzde-oCeeDSypCxruugwp2PBo4'
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def message_handler(message):
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
