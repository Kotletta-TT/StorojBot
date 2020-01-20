import time
import datetime
import psycopg2
from parser_p import parser_pages as get_avito

ONE_MINUTE = 60
REQUEST_DELAY = ONE_MINUTE * 5  # время между зпросами (300 по умолчанию)
DEFAULT_AVITO_URL = 'https://www.avito.ru/rossiya/tovary_dlya_kompyutera/komplektuyuschie/videokarty?s_trg=11&cd=1&s=104'
SNDTXT = None

# Блок  поиска новых обьявлений путем отсеивания ID
# На данный момент неиспользуется, т.к. неактуальна 
# Поиск и парсинг по времени оказался быстрее и точнее.

def check_new():
    source_avito = get_avito(count_pages=1)
    get_key = []
    for key in source_avito.keys():
        get_key.append(key)

    time.sleep(10)

    check_avito = get_avito(count_pages=1)
    check_key = []
    for new_key in check_avito.keys():
        check_key.append(new_key)

    print(get_key)
    print('\n')
    print(check_key)
    result = [x for x in check_key if x not in get_key]
    unresult = [x for x in get_key if x in check_key]
    print(result)
    print(unresult)


# Блок поиска и парсинга объявлений по времени,
# На данный момент работает и используется в коде
def check_new_time(dbname, dbuser, url=DEFAULT_AVITO_URL, count_p=2):  # Передаем, ссылку и количество страниц указанное пользователем
    conn = psycopg2.connect('dbname=' + dbname + ' user=' + dbuser)
    cur = conn.cursor()

    source_dict = {}
    source_avito = get_avito(url, count_p)  # Первый эталонный запрос(источник для парсинга)
    source_dict.update(source_avito)
    for oneString in source_dict.items():
        #print(oneString)
        dateplustime = ' '.join(oneString[1][3])
        cur.execute('INSERT INTO ads (id_ads, adname, price, city, url, addate) VALUES (%s, %s, %s, %s, %s, %s);', (oneString[0], oneString[1][0], oneString[1][1], oneString[1][2], oneString[1][4], dateplustime))
    conn.commit()
    conn.close()

    while True:
        check_dict = {}

        today = datetime.date.today().strftime("%d %B")  # Находимм "Сегодня"
        totime = datetime.datetime.now().strftime("%H:%M")  # Находим "Сейчас"
        totime_sec = convert_secs(totime)  # Конвертация времени в секунды
        time.sleep(REQUEST_DELAY)  # !!!!!!!!!!!!!!!! ТАЙМЕР ПРОВЕРКИ ТУТ!!!!!!!!!!!!!!!!
        check_avito = get_avito(url, count_p)  # Новый запрос "Проверка новых объявлений"
        check_dict.update(check_avito)
        conn = psycopg2.connect('dbname=' + dbname + ' user=' + dbuser)
        cur = conn.cursor()
        # Парсинг новых обьявлений по времени
        for i in check_dict.items():

            check_new_date = i[1][3][0]

            if check_new_date == today:

                check_new_time = i[1][3][1] # Если ошибка out of range, смотреть в parser_p 69 строка
                sec = convert_secs(check_new_time)
                # Условие верно, при разницы между временем запроса и временем объявления,
                # Не более чем на 600сек (10мин)
                if sec >= totime_sec - 600:
                    # Если нет в словаре-источнике(первом эталонном запросе)
                    if i not in source_dict.items():
                        dateplustime = ' '.join(i[1][3])

                        cur.execute('INSERT INTO ads (id_ads, adname, price, city, url, addate) VALUES (%s, %s, %s, %s, %s, %s);', (i[0], i[1][0], i[1][1], i[1][2], i[1][4], dateplustime))
                        source_dict[i[0]] = i[1]
                        print(len(source_dict))

        conn.commit()
        conn.close()


def convert_secs(ttime):
    conv_sec = ttime.split(':')
    sec_sum = int(conv_sec[0]) * 3600 + int(conv_sec[1]) * 60
    return sec_sum
