import random
import time
import telebot
import requests
from bs4 import BeautifulSoup

import config
import database

bot = telebot.TeleBot(config.BOT_TOKEN)
database = database.Database()

@bot.message_handler(commands=['reg'])
def reg(message):
    user = database.set_user(message)
    bot.send_message(message.chat.id, f'{user}\n\n<b>Доступные команды:</b>\n/stats\n/set_name (name)', parse_mode='HTML')

@bot.message_handler(commands=['set_name'])
def set_name(message):
    user_parameters = message.text.split(maxsplit=1)
    if len(user_parameters) != 2:
        bot.reply_to(message, '⚠️ Вы не указали имя!')
        return
    else:
        user = list(database.get_user(message.from_user.id))
        user[1] = user_parameters[1]
        bot.reply_to(message, database.update_user(user))

@bot.message_handler(commands=['stats'])
def stats(message):
    user = database.get_user(message.from_user.id)
    bot.reply_to(message, f'ℹ️ Информация об <a href="tg://user?id={user[0]}">{user[1]}</a>:\n'
                          f'💦 Кончил: {user[2]} раз\n'
                          f'🔞 Поебался: {user[3]} раз', parse_mode='HTML')

@bot.message_handler(commands=['meme'])
def meme(message):
    url = 'https://www.anekdot.ru/random/mem/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        topicboxes = (soup.findAll('div', class_='topicbox'))
        topicbox = random.choice(topicboxes)
        mem = topicbox.find('img')['src']
        if 'jpg' in mem or 'png' in mem:
            bot.send_photo(message.chat.id, mem, parse_mode='HTML')
        elif 'gif' in mem or 'mp4' in mem:
            bot.send_video(message.chat.id, mem, parse_mode='HTML')
    except:
        meme(message)

@bot.message_handler(commands=['anekdot'])
def anekdot(message):
    url = 'https://baneks.site/random'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    anekdot = (soup.find('div',
                        class_='block-content mdl-card__supporting-text mdl-color--grey-300 mdl-color-text--grey-900').find('p'))
    str_anekdot = anekdot.get_text()
    bot.send_message(message.chat.id, '<b>🤣 Анедкот</b>\n\n' + str_anekdot, parse_mode='HTML')

@bot.message_handler(commands=['cum'])
def cum(message):
    user = list(database.get_user(message.from_user.id))
    if user is None:
        bot.send_message(message.chat.id, '⚠️ Пользователь не зарегистрирован')
        return

    if random.randint(0, 6) >= 3:
        response = requests.get("https://g.tenor.com/v1/search?q=cum&key=LIVDSRZULELA&limit=50")
        data = response.json()
        cum_gif = random.choice(data["results"])['media'][0]['gif']['url']
        text = message.text.split(maxsplit=1)
        if len(text) == 2:
            bot.send_animation(message.chat.id, cum_gif, caption=f'💦 Вы кончили на {text[1]}',
                                   parse_mode='HTML')
        elif message.reply_to_message is not None:
            cum_user = database.get_user(message.reply_to_message.from_user.id)
            if cum_user is None:
                bot.send_message(message.chat.id, '⚠️ Пользователь не зарегистрирован')
                return
            bot.send_animation(message.chat.id, cum_gif, caption=f'💦 Вы кончили на <a href="tg://user?id={user[0]}">{user[1]}</a>', parse_mode='HTML')
        user[2] = user[2] + 1
        print(user)
        database.update_user(user)
    else:
        sad_response = requests.get("https://g.tenor.com/v1/search?q=lonely&key=LIVDSRZULELA&limit=50")
        sad_data = sad_response.json()
        sad_gif = random.choice(sad_data["results"])['media'][0]['gif']['url']
        bot.send_animation(message.chat.id, sad_gif, caption=f'😞 У вас все получится', parse_mode='HTML')

@bot.message_handler(commands=['want'])
def want(message):
    who = message.text.split(maxsplit=1)[1]
    bot.send_message(message.chat.id, f'Как же я хочу {who}, ее нетронутая некем тело, это невинное милое создание. Никем нецелованная и никем не трахана, как же я хочу войти в ее упргую попку, и оттрахать, чтобы она нежно станола и в конце у нее треслись ножки, и дрожали ручки, чтобы она просила еще и еще до потери пульса, в порше, в  душе, на кухне, в зале, в спальне, на улице, в колледже')

if __name__ == '__main__':
    print('----------------Bot start-----------------\n')
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(3)