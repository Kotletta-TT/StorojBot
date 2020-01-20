from bs4 import BeautifulSoup
import requests
import datetime
import locale
import re
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def parser_pages(url='https://www.avito.ru/sochi/tovary_dlya_kompyutera/komplektuyuschie/videokarty?s_trg=11&cd=1', count_pages=2):
    data_dict = {}
    request = requests.get(url, timeout=5)
    soup = BeautifulSoup(request.content, 'lxml')
    #Пока не могу нормально получить количество страниц с авито поэтому данная часть закоментированна
    #Просто забираю пока первые 2 страницы
    #ads_count_pages = math.ceil(int(soup.find('span', {'class':'page-title-count'}))).get_text().replace(" ",'')) / 50)
    #ads_count_pages = soup.find('div', {'class': 'js-pages pagination-pagination-2j5na'}).get_text().replace(' ','')
    #print(ads_count_pages)
    #if ads_count_pages > count_pages:
    #    ads_count_pages = count_pages
    for count_p in range(count_pages):  #ads_count_pages):
        count_p += 1
        url_p = url.split('?')
        url_plus = url_p[0] + '?p={}&'.format(count_p) + url_p[1]

        request_page = requests.get(url_plus, timeout=5)
        soup = BeautifulSoup(request_page.content, 'lxml')




        ads_container = soup.find_all('div', {"class":"item_table-wrapper"})
        for container in ads_container:
            pre_data_list = []

            try:
                ads_name = container.find('a', {"class":"snippet-link"}).get_text().split('\n')[1]
                pre_data_list.append(ads_name)

            except:
                ads_name = ''
                pre_data_list.append(ads_name)

            try:
                ads_price = container.find('span', {'class':"price"}).get_text()
                pre_current_price = re.findall('(\d+)', ads_price)
                current_price = ''.join(pre_current_price)
                pre_data_list.append(current_price)

            except:
                current_price = ''
                pre_data_list.append(current_price)

            try:
                ads_city = container.find('span', {'class':'item-address-georeferences-item__content'}).get_text()
                pre_data_list.append(ads_city)

            except:
                try:
                    ads_city = container.find('span', {'class':'item-address__string'}).get_text().split('\n')[1]
                    pre_data_list.append(ads_city)

                except:
                    ads_city = 'bug_parser'
                    pre_data_list.append(ads_city)

            try:
                current_time = []
                ads_time = container.find('div', {'class':"js-item-date c-2"})
                full_bugs_time = ads_time['data-absolute-date'].strip()
                current_time = full_bugs_time.split(' ') # если не разделяет время, вместо пробела поставить \xa0
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
            

            ads_url = container.find('a', {'class':'snippet-link'})
            current_url = "https://www.avito.ru"+ ads_url['href']
            pre_data_list.append(current_url)


            ads_id = ads_url['href'].split('_')[-1]
            if '?' in ads_id:
                current_ads_id = ads_id.split('?')[0]
            else:
                current_ads_id = ads_id

            data_dict[current_ads_id] = pre_data_list





    return data_dict