import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb://yeny:yeny@3.35.22.81', 27017)
db = client.dbjungle

def get_urls():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://movie.naver.com/movie/sdb/rank/rpeople.nhn'

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    target = soup.select('#old_content > table > tbody > tr > .title > a')
    urls = []
    for one in target:
        base_url = 'https://movie.naver.com'
        actor_url = base_url + one['href']
        urls.append(actor_url)

    return urls


def insert_star(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_last = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)')

    url_image = og_image['content']
    url_title = og_title['content']
    url_last = og_last.text

    doc = {
        'name': url_title,
        'img_url' : url_image,
        'last' : url_last,
        'url' : url,
        'like' : 0
    }

    db.mystar.insert_one(doc)
    print('완료!', url_title)


def insert_all():
    db.mystar.drop() #mystar 모두 지움
    urls = get_urls()
    for url in urls:
        insert_star(url)


insert_all()



