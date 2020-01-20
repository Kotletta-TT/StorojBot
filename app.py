import telebot
import time
import threading
import psycopg2
import re
import json
from func import get_token as token
from func import get_proxy as proxy
#from func import check_url as check_url
from test import check_new_time as start_storozj



PROXY = proxy()
TOKEN = token()
dbname = 'storojdb'
dbuser = 'storoj'
counter = ''
bot = telebot.TeleBot(TOKEN)
telebot.apihelper.proxy = {'https': PROXY}




@bot.message_handler(commands=['start'])
def send_welcome(message):
	chatid = message.chat.id
	bot.reply_to(message, '''Привет, я бот-сторож для Авито, я буду "сторожить" авито и если что то появится по твоей 
	теме, я тебя оповещу и ты сможешь первым отреагировать на новые объявления''')
	time.sleep(3)
	bot.send_message(chatid, '''просто отправь /url "ссылка на товар или группу товаров в твоем городе или по россии" ''')


@bot.message_handler(commands=['url'])
def start_url(message):
	global counter
	chatid = message.chat.id
	url = message.text.split()[1]
	bot.send_message(chatid, 'Ссылка корректна!')
	time.sleep(2)
	bot.send_message(chatid, '''Я просканирую первые страницы и буду ждать новых объявлений, в случае появления - я вам все пришлю''')
	t1 = threading.Thread(target=thread_start_storj, args=(dbname, dbuser, url))
	t1.start()
	time.sleep(10)
	conn = psycopg2.connect('dbname=' + dbname + ' user=' + dbuser)
	cur = conn.cursor()
	cur.execute('SELECT max(id) FROM ads;')
	a = cur.fetchall()
	pre_counter = re.findall('(\d+)', str(a[0]))
	counter = int(pre_counter[0])
	conn.commit()
	conn.close()
	while True:
		time.sleep(10)
		conn = psycopg2.connect('dbname=' + dbname + ' user=' + dbuser)
		cur = conn.cursor()
		cur.execute('SELECT max(id) FROM ads;')
		a = cur.fetchall()
		pre_counter = re.findall('(\d+)', str(a[0]))
		new_count = int(pre_counter[0])
		if new_count > counter:
			count_new_ads = new_count - counter
			str_new_ads = str(count_new_ads)
			cur.execute('SELECT * FROM ads ORDER BY id DESC LIMIT %s;', (str_new_ads,))
			new_ads = cur.fetchall()
			for one_ad in new_ads:
				#str_ad = str(one_ad)
				snd_txt = json.dumps(one_ad, ensure_ascii=False)
				bot.send_message(chatid, snd_txt)
			counter = new_count
		conn.commit()
		conn.close()


def thread_start_storj(dbname, dbuser, url):
	time.sleep(5)
	start_storozj(dbname, dbuser, url)



bot.polling()

