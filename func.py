import requests
import re
import os


def url_or_answer(answer_string):
    if  'avito.ru' in answer_string:

        if '?' in answer_string:
            url_list = answer_string.split('?')
            url_list.insert(1, '?')
            return url_list
        else:
            url_clear = []
            url_clear.append(answer_string)
            return url_clear
    else:
        url_create = ['https://www.avito.ru/rossiya?']
        if " " in answer_string:
            answ_changed = '+'.join(answer_string.split(' '))
            url_create.append('q=')
            url_create.append(answ_changed)
            return url_create
        else:
            url_create.append('q=')
            url_create.append(answer_string)
            return url_create


def check_url(url):

    request = str(requests.get(url).status_code)
    if '200' in request:
        return url
    else:
        print('bad')  #Ссылка недействительна, отправить сообщение пользователю

def full_check(url):
    url = ''.join(url_or_answer(message))
    check_url_acess = check_url(url)
    #Что то возвращать после полной проверки! Если все хорошо url_list, если плохо
    #Думаю про обработчик ошибок try..except



def get_token():
    config = configparser.ConfigParser()
    path_conf = 'settings.cfg'
    config.read(path_conf)
    tele_token = config.get('Telegram_Token', 'Token')
    return tele_token

def get_Updates(token=get_token()):
    bot_api = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'getUpdates')
    request = requests.get_json(bot_api) # Изменил с get на get_json надо проверить
    s = request.json() #Если вариант выше заработает то не нужна
    return request

def editMessageText(chat_id, message, message_id, parser_buttons, token=get_token()):
    bot_api = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'editMessageText')
    js_answer = {'text':message, 'chat_id':chat_id, 'message_id':message_id, "reply_markup":{"inline_keyboard":[parser_buttons]}}
    request = requests.post(bot_api, json=js_answer)
    a = request.text                   #Эти две строки для проверки что,
    print('!SEND123!\n'+ a +'!SEND123!\n')

def send_Message(chat_id, message, inl_keyb='None', token=get_token()):

    bot_api = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage')
    #js_answer={'text':message, 'chat_id':chat_id, 'parse_mode':'Markdown', 'disable_web_page_preview':'true'} # Строка для форматирования текста и убирания превью URLa
    if inl_keyb not in 'None':
        js_answer={'text':message, 'chat_id':chat_id, 'reply_markup': create_kbrd(inl_keyb)}
    else:
        js_answer={'text':message, 'chat_id':chat_id}
        #print('!JS_ANSW!\n'+str(js_answer)+'\n') #Проверка сборки JSON
    request = requests.post(bot_api, json=js_answer)
    a = request.text                   #Эти две строки для проверки что,
    #print('!SEND!\n'+ a +'!SEND!\n')   #бот отправил в формате JSON
    
        

def create_kbrd(name_keyboard):
    
    reply_mup_array = {'start':{"inline_keyboard":[[{"text":"Storoj","callback_data":"storoj_bot"},{"text":"AutoLoad","callback_data":"auto_load"}]]}}
    if name_keyboard in reply_mup_array:
        return reply_mup_array[name_keyboard]
