import requests
from bs4 import BeautifulSoup
import pprint
import json
import pandas as pd

index = range(0, 250, 25)
index = list(index)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}


def download_all_htmls():
    """下载所有urls"""
    html = []
    for indexes in index:
        url = f'https://movie.douban.com/top250?start={indexes}&filter='
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            raise Exception('error')
        text = request.text
        html.append(text)
    return html


htmls_text = download_all_htmls()

def parse_single_html(html):

    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('div', class_='article')
    ol = article.find('ol', class_='grid_view')
    items = ol.find_all('div', class_='item')
    data = []
    for item in items:
        rank = item.find('div', class_='pic').find('em').get_text()
        info = item.find('div', class_='info')
        title = info.find('div', class_='hd').find('a').find('span', class_='title').get_text()
        star = info.find('div', class_='bd').find('div', class_='star')
        spans = star.find_all('span')
        rating_star = spans[0]['class'][0]
        rating_num = spans[1].get_text()
        comments = spans[3].get_text()
        data.append({'rank': rank, 'title': title, 'rating_star': rating_star.replace('rating', '').replace('-t', ''), 'rating_num': rating_num, 'comments': comments.replace('人评价', '')})
    return data

final_data = []

for urls in htmls_text:
    final_data.extend(parse_single_html(urls))

df = pd.DataFrame(final_data)

df.to_excel('/Users/linpeng/PycharmProjects/Python crawl/test/utils/blog_test/Book1.xlsx')
