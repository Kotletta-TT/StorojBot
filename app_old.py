from flask import Flask
from flask import request
from flask_debugtoolbar import DebugToolbarExtension
import test as my_test
import func

app = Flask(__name__)
app.debug = True

app.secret_key = 'development key'

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    # return 'Hello, World!'
    if request.method == 'POST':

        dat_json = request.get_json()
        if 'callback_query' in dat_json.keys():
            chat_id = dat_json['callback_query']['message']['chat']['id']
            message = dat_json['callback_query']['message']['text']
            message_id = dat_json['callback_query']['message']['message_id']
            data = dat_json['callback_query']['data']

            if 'storoj_bot' == data:
                # parser_buttons = [{"text":"URL","callback_data":"url_pars"},{"text":"Запрос","callback_data":"zapros_pars"}]
                func.send_Message(chat_id,
                                  'Запуск сторожа. Введите URL-ссылку на Авито, либо запрос (учтите запрос идет по дефолтной ссылке авито - по Всей России, по всем категориям)')
            if 'auto_load' == data:
                storoj_buttons = [{"text": "URL", "callback_data": "url_pars"},
                                  {"text": "Запрос", "callback_data": "zapros_storoj"}]
                func.editMessageText(chat_id, 'Запуск Автозагрузки', message_id, storoj_buttons)
        else:
            chat_id = dat_json['message']['chat']['id']
            message = dat_json['message']['text']
            if '/start' == message:
                func.send_Message(chat_id, 'Чем я могу помочь?', 'start')
            elif '/help' == message:
                func.send_Message(chat_id, 'Бот такой то, может то то, команды такие')
            elif '/url https://www.avito.ru/' in message:
                clr_url = message.split(' ')[1]
                my_test.check_new_time(clr_url, chat_id)
            else:
                func.send_Message(chat_id, 'Не неси чепухи набирай, /start, или /help')

        # func.send_Message(chat_id, message)

    return '<h1>Storoj Bot</h1>'


if __name__ == '__main__':
    app.run(debug=True)
