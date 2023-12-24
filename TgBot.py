import random
import telebot

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
bot = telebot.TeleBot('6897471229:AAHikhuUnEYPrcInaCF0N9WzK_0E2uenjck')

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 10

# Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хэндлер будет срабатывать на команду "/start"
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет!\n')
    bot.send_message(message.chat.id, f'(*^ω^)\n')
    bot.send_message(message.chat.id, f'Давайте сыграем в игру "Угадай число"?\n')
    bot.send_message(message.chat.id, f'Чтобы получить правила игры и список доступных\n')
    bot.send_message(message.chat.id, f'команд - отправьте команду /help')


# Этот хэндлер будет срабатывать на команду "/help"
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Правила игры:\n\nЯ загадываю число от 1 до 100, ')
    bot.send_message(message.chat.id, f'а вам нужно его угадать\n')
    bot.send_message(message.chat.id, f'o(>ω<)o\n')
    bot.send_message(message.chat.id, f'У вас есть {ATTEMPTS} попыток\n ')
    bot.send_message(message.chat.id, f'Доступные команды:\n/help - правила ')
    bot.send_message(message.chat.id, f'/stat - посмотреть статистику\n\nДавай сыграем?\n')
    bot.send_message(message.chat.id, f'/start_game - запустить игру')


# Этот хэндлер будет срабатывать на команду "/stat"
@bot.message_handler(commands=['stat'])
def stat(message):
    bot.send_message(message.chat.id, f'Всего игр сыграно: {user["total_games"]}\n')
    bot.send_message(message.chat.id, f'Игр выиграно: {user["wins"]}')
    bot.send_message(message.chat.id, f'(⊙_⊙)')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@bot.message_handler(commands=['start_game'])
def play_game(message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        bot.send_message(message.chat.id, 'Ура!\n\nЯ загадал число от 1 до 100, ')
        bot.send_message(message.chat.id, 'попробуй угадать!')

    else:
        bot.send_message(message.chat.id, 'Пока мы играем в игру я могу ')
        bot.send_message(message.chat.id, 'реагировать только на числа от 1 до 100 ')
        bot.send_message(message.chat.id, 'и команду /stat')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@bot.message_handler(func=lambda message: True)
def game(message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            bot.send_message(message.chat.id, 'Ура!!! Вы угадали число!\n\n')
            bot.send_message(message.chat.id, 'Может, сыграем еще?')
            bot.send_message(message.chat.id, '/start_game')

        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            bot.send_message(message.chat.id, 'Мое число меньше  ╮( ˘ ､ ˘ )╭')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            bot.send_message(message.chat.id, 'Мое число больше  ┐(‘～` )┌')

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1

            bot.send_message(message.chat.id, f'К сожалению, у вас больше не осталось попыток. ')
            bot.send_message(message.chat.id, f'Вы проиграли :(\n')
            bot.send_message(message.chat.id, f'Мое число было {user["secret_number"]}\n')
            bot.send_message(message.chat.id, f'Давайтесыграем еще?')
            bot.send_message(message.chat.id, '/start_game')

    else:
        bot.send_message(message.chat.id, 'Мы еще не играем. Хотите сыграть?')
        bot.send_message(message.chat.id, '/start_game')


if __name__ == '__main__':
    bot.polling()
