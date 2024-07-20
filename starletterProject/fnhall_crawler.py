import requests, os
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "starletterProject.settings")
import django
django.setup()

from funeralhalls.models import FuneralHall


def get_funeralhall_data():
    result = []

    url = 'https://www.animal.go.kr/front/awtis/shop/undertaker1List.do?totalCount=75&pageSize=10&&page=1'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find("li", {"class": "page-mark"}).find('span').decompose()
    page_list = soup.find('li', {'class': 'page-mark'}).text

    for pagnum in range(1, int(page_list)+1):
        url = 'https://www.animal.go.kr/front/awtis/shop/undertaker1List.do?totalCount=75&pageSize=10&&page=' + str(pagnum)
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        list_items = soup.find('tbody').findAll('tr')

        for item in list_items:
            original_id = item.find("th", {'data-title': '번호'}).text
            original_id = int(original_id)

            name = item.find("td", {'data-title': '업체명'}).text

            location = item.find("td", {'data-title': '소재지'}).text
            location = location.strip()

            contact = item.find("td", {'data-title': '전화번호'}).text
            if '*' in contact:
                contact = ''

            link = item.find("td", {'data-title': '홈페이지'}).text
            link = link.strip()
            if link == '-':
                link = ''
            
            raw_tags = item.find('td', {'data-title': '취급업종'}).text
            raw_tags = raw_tags.split(',')
            tags = []
            for tag in raw_tags:
                tag = tag.strip()
                if tag == '장례':
                    tags.append('장례')
                elif tag == '화장':
                    tags.append('화장')
                elif tag == '봉안':
                    tags.append('봉안')
                elif tag == '건조':
                    tags.append('건조')

            item_obj = {
                'original_id' : original_id,
                'name' : name,
                'location' : location,
                'contact' : contact,
                'link' : link,
                'tag' : tags,
            }

            result.append(item_obj)

    return result



def add_new_items(crawled_items):
    last_inserted_item = FuneralHall.objects.last()
    if last_inserted_item is None:
        last_inserted_id = ""
    else:
        last_inserted_id = getattr(last_inserted_item, 'original_id')

    items_to_insert_into_db = []
    for item in crawled_items:
        if item['original_id'] == last_inserted_id:
            break
        items_to_insert_into_db.append(item)
    items_to_insert_into_db.reverse()

    for item in items_to_insert_into_db:
        print("new item added : " + item['name'])

        FuneralHall(original_id=item['original_id'],
                    name=item['name'],
                    location=item['location'],
                    contact=item['contact'],
                    link=item['link'],
                    tag=item['tag'],
                    ).save()

    return items_to_insert_into_db



if __name__ == '__main__':
    add_new_items(get_funeralhall_data())
