import time
import datetime
import func
import json
from parser_p import parser_pages as get_avito

ONE_MINUTE = 60
REQUEST_DELAY = ONE_MINUTE * 5  # время между зпросами (300 по умолчанию)
DEFAULT_AVITO_URL = 'https://www.avito.ru/rossiya/tovary_dlya_kompyutera/komplektuyuschie/videokarty?s_trg=11&cd=1&s=104'


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
def check_new_time(
        url=DEFAULT_AVITO_URL,
        chat_id='719714331', count_p=2):  # Передаем, ссылку и количество страниц,
    source_dict = {}  # Указанное пользователем
    source_avito = get_avito(url, count_p)  # Первый эталонный запрос(источник для парсинга)
    source_dict.update(source_avito)

    while True:
        check_dict = {}

        today = datetime.date.today().strftime("%d %B")  # Находимм "Сегодня"
        totime = datetime.datetime.now().strftime("%H:%M")  # Находим "Сейчас"
        totime_sec = convert_secs(totime)  # Конвертация времени в секунды
        time.sleep(REQUEST_DELAY)  # !!!!!!!!!!!!!!!! ТАЙМЕР ПРОВЕРКИ ТУТ!!!!!!!!!!!!!!!!
        check_avito = get_avito(url, count_p)  # Новый запрос "Проверка новых объявлений"
        check_dict.update(check_avito)
        # Парсинг новых обьявлений по времени
        for i in check_dict.items():

            check_new_date = i[1][3][0]

            if check_new_date == today:

                check_new_time = i[1][3][1]
                sec = convert_secs(check_new_time)
                # Условие верно, при разницы между временем запроса и временем объявления,
                # Не более чем на 600сек (10мин)
                if sec >= totime_sec - 600:
                    # Если нет в словаре-источнике(первом эталонном запросе)
                    if i not in source_dict.items():

                        snd_txt = json.dumps(i, ensure_ascii=False)
                        func.send_Message(chat_id, snd_txt)
                        source_dict[i[0]] = i[1]
                        print(len(source_dict))
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue


def convert_secs(ttime):
    conv_sec = ttime.split(':')
    sec_sum = int(conv_sec[0]) * 3600 + int(conv_sec[1]) * 60
    return sec_sum

    # def storoj(url, chat_id, message, count_p=2):
    #     source_avito = get_avito(url, count_p) # Первый эталонный запрос(источник для парсинга)
    #     while True: # Бесконечный цикл на тайминге внутри!
    #         # (НАДО ЕГО КАК ТО ПРЕРВАТЬ ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ)
    #         check_new_time(url, count_p, source_avito)
    #         func.send_Message(chat_id, text)


if __name__ == '__main__':
    check_new_time()
