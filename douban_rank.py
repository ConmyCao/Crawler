import json

import requests
import re


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return 'GET HTML ERROR!'


def parse_page(html):
    pattern = re.compile('<em class="">(.*?)</em>.*?<a href="(.*?)">.*?<img .*?>.*?</a>.*?</div>.*?<div class="info">.*?<div class="hd">.*?<a .*?>.*?<span class="title">(.*?)</span>.*?<span class="title">&nbsp;/&nbsp;.*?</span>.*?<span class="other">&nbsp;/&nbsp;.*?</span>.*?</a>.*?</div>.*?<div class="bd">.*?<p class="">.*?导演: (.*?)&nbsp;&nbsp;&nbsp;主演: .*?<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?<div class="star">.*?<span class="rating45-t"></span>.*?<span class="rating_num" property="v:average">(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'rank': item[0],
            'href': item[1],
            'name': item[2],
            'director': item[3].strip()[4:],
            'year': item[4].strip(),
            'country': item[5].strip(),
            'style': item[6].strip(),
            'score': item[7].strip()
        }


def write_to_file(content):
    #写入文件函数
    with open('result.txt', 'a', encoding='utf-8') as file:
        file.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    # for res in parse_page(get_page('https://movie.douban.com/top250')):
    #     write_to_file(res)

    for i in range(10):
        # url = 'https://movie.douban.com/top250'
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter'
        for res in parse_page(get_page(url)):
            write_to_file(res)