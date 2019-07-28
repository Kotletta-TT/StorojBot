from bs4 import BeautifulSoup
import requests
import lxml
import json
import math
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

#ads_container = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
#print(ads_container)


def parser_pages(url='https://www.avito.ru/sochi/tovary_dlya_kompyutera/komplektuyuschie/videokarty?s_trg=11&cd=1', count_pages=2):
    data_dict = {}
    #id = 0
    request = requests.get(url, timeout=5)
    soup = BeautifulSoup(request.content, 'lxml')


    ads_count_pages = math.ceil(int(soup.find('span', {'class':'page-title-count'}).get_text().replace(" ",'')) / 50)
    if ads_count_pages > count_pages:
        ads_count_pages = count_pages
    for count_p in range(ads_count_pages):
        count_p += 1
        url_p = url.split('?')
        url_plus = url_p[0] + '?p={}&'.format(count_p) + url_p[1]

        request_page = requests.get(url_plus, timeout=5)
        soup = BeautifulSoup(request_page.content, 'lxml')




        ads_container = soup.find_all('div', {"class":"item_table-wrapper"})
        for container in ads_container:
            pre_data_list = []
            #id += 1

            try:
                ads_name = container.find('span', {"itemprop":"name"}).get_text()
                pre_data_list.append(ads_name)

            except:
                ads_name = ''
                pre_data_list.append(ads_name)

            try:
                ads_price = container.find('span', {'class':"price"})
                current_price = ads_price['content']
                pre_data_list.append(current_price)

            except:
                current_price = ''
                pre_data_list.append(current_price)

            try:
                ads_city = container.find('div', {'class':'data'}).find_all('p')[-1].get_text()
                pre_data_list.append(ads_city)

            except:
                ads_city = ''
                pre_data_list.append(ads_city)

            try:
                current_time = []
                ads_time = container.find('div', {'class':"js-item-date c-2"})
                full_bugs_time = ads_time['data-absolute-date'].strip()
                current_time = full_bugs_time.split('\xa0')
                day = str(current_time[0])
                                
                if 'Сегодня' in day:

                    current_time[0] = datetime.date.today().strftime("%d %B")
                
                elif 'Вчера' in day:
                    yesterday = datetime.date.today() - datetime.timedelta(days=1)
                    current_time[0] = yesterday.strftime("%d %B")
                 
                pre_data_list.append(current_time)



            except:
                current_time = ''
                pre_data_list.append(current_time)
            

            ads_url = container.find('a', {'class':'item-description-title-link'})
            current_url = "https://www.avito.ru"+ ads_url['href']
            pre_data_list.append(current_url)


            ads_id = ads_url['href'].split('_')[-1]
            if '?' in ads_id:
                current_ads_id = ads_id.split('?')[0]
            else:
                current_ads_id = ads_id
            #pre_data_list.append(ads_id)
            data_dict[current_ads_id] = pre_data_list




    #a = json.dumps(data_dict, ensure_ascii=False)
    return data_dict
    #with open('data.json', 'a', encoding='utf-8') as json_dict:
    #    json.dump(data_dict, json_dict, ensure_ascii=False)


#if __name__ == '__main__':
    #parser_pages()

# biriji = parser_page()
# print(biriji)


    #
    #     json.dumps(info_dict, json_dict, ensure_ascii=False)



    #print(current_price, ads_name, ads_city, current_time, current_url)
