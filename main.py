import requests
from bs4 import BeautifulSoup as bs
import telebot

def get_weather(town):
    url = 'https://sinoptik.ua/погода-' + town

    session = requests.Session()
    request = session.get(url, headers = headers)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        table = soup.find('table', attrs = {'class': 'weatherDetails'})
        tr = table.find('tr', attrs = {'class': 'img'})
        td = tr.find('td', attrs = {'class': 'cur'})
        weather = td.find('div', attrs = {'class': 'weatherIco'})['title']

        temp = soup.find('p', attrs = {'class': 'today-temp'}).text

        return temp + ', ' + weather

    else:
        return False

def get_crypto(coin):
    url = 'https://minfin.com.ua/currency/crypto/'

    session = requests.Session()
    request = session.get(url, headers = headers)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')

        res = False
    
        if coin == 'BTC':
            btc = soup.find('div', attrs = {'class': 'coin-item', 'title': 'Bitcoin'})
            res = btc.findNext('div')['data-sort-val'] + 'USD'

        if coin == 'ETH':
            btc = soup.find('div', attrs = {'class': 'coin-item', 'title': 'Ethereum'})
            res = btc.findNext('div')['data-sort-val'] + 'USD'

        if coin == 'LTC':
            btc = soup.find('div', attrs = {'class': 'coin-item', 'title': 'Litecoin'})
            res = btc.findNext('div')['data-sort-val'] + 'USD'

        return res

    else:
        return False

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

prevMessages = {}

bot = telebot.TeleBot("893022267:AAHN8MEQX2t3BPLqtHGIZlQOj7Y-hLLsoVk")

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    answer = 'Чтобы узнать погоду напишите команду /weather. Чтобы узнать стоимость криптовалют напишите команду /crypto.'
    bot.send_message(cid, answer)
    prevMessages[cid] = m.text

@bot.message_handler(commands=['weather'])
def command_weather(m):
    cid = m.chat.id
    answer = 'Отлично! Теперь укажите город:'
    bot.send_message(cid, answer)
    prevMessages[cid] = m.text

@bot.message_handler(commands=['crypto'])
def command_crypto(m):
    cid = m.chat.id
    answer = 'Отлично! Теперь укажите валюту(BTC, ETH, LTC):'
    bot.send_message(cid, answer)
    prevMessages[cid] = m.text

@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_text(m):
    cid = m.chat.id
    if prevMessages[cid] == '/weather':
        weather = get_weather(m.text)
        bot.send_message(cid, weather)
    if prevMessages[cid] == '/crypto':
        crypto = get_crypto(m.text)
        bot.send_message(cid, crypto)
    prevMessages[cid] = m.text

bot.polling()