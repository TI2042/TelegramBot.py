import random
import re
import requests
import telebot

from bs4 import BeautifulSoup as BS
import config

bot = telebot.TeleBot(config.Token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Данный бот может рассказать погоду на ближайшие 2 дня в городе" +
                         " Ульяновск (для этого команда \"Погода\"). Так же бот может помочь" +
                         " с принятием решения (для этого нужно лишь задать вопрос с предпологаемыми ответами \"Да\" " +
                         "или \"Нет\").")
    elif message.text == "Погода":
        weather(message)
    elif re.fullmatch('[A-z,А-я,0-9\s]+\?', message.text):
        ball_eight(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# погода
def weather(message):
    url = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A3%D0%BB%D1%8C%D1%8F%D0%BD%D0%BE%D0%B2%D1%81%D0%BA%D0%B5'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'
                      'Chrome/64.0.3282.167 Safari/537.36'
    }
    result = requests.get(url, headers=headers)
    soup = BS(result.content, 'html.parser')
    match = soup.find('meta', attrs={'name': 'description'})
    bot.send_message(message.chat.id, f"Прогноз погоды на сегодня и завтра:\n {match.attrs['content']}")


# волшебный шар восьмёрка
def ball_eight(message):
    answers = {'Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да', 'Можешь быть уверен в этом',
               'Мне кажется — да', 'Вероятнее всего', 'Хорошие перспективы',
               'Знаки говорят — да', 'Да', 'Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать',
               'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять', 'Даже не думай',
               'Мой ответ — «нет»', 'По моим данным — «нет»', 'Перспективы не очень хорошие', 'Весьма сомнительно'}
    bot.send_message(message.chat.id, f"Шар говорит:\n {random.sample(answers, 1)}")


bot.polling(none_stop=True, interval=0)
