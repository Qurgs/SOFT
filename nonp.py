import telebot


token = '7021680026:AAGzp5bCgP7nu5YCIwBgaMkRBgR0K-UuPRk'
bot = telebot.TeleBot(token)

#Мы используем словарь room_dict, потому что он позволяет нам хранить информацию о комнатах, каждая из которых имеет уникальное название. Ключи словаря представляют собой названия комнат, а значения содержат информацию о каждой комнате, например, кто ее создал и кто участвует в ней.
room_dict = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, это бот!")


@bot.message_handler(commands=["create"])
def create(message):
    room_name = message.text.split("/create ", 1)[1]  # Получаем название комнаты из сообщения
    room_dict[room_name] = {'creator_id': message.chat.id, 'participants': {message.chat.id: message.from_user.username}}
    bot.send_message(message.chat.id, f"Комната '{room_name}' создана.")

@bot.message_handler(commands=["join"])
def join(message):
    room_name = message.text.split("/join ", 1)[1]  # Получаем название комнаты из сообщения
    if room_name not in room_dict:
        bot.send_message(message.chat.id, f"Комнаты '{room_name}' не существует.")
    elif len(room_dict[room_name]['participants']) >= 2:
        bot.send_message(message.chat.id, f"В комнате '{room_name}' уже максимальное количество участников.")
    else:
        room_dict[room_name]['participants'][message.chat.id] = message.from_user.username
        bot.send_message(message.chat.id, f"Вы присоединились к комнате '{room_name}'.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    for room_name, room_info in room_dict.items():
        if message.chat.id in room_info['participants']:
            for participant_id, username in room_info['participants'].items():
                if participant_id != message.chat.id:
                    bot.send_message(participant_id, f" {message.text}")
            break


bot.polling()
