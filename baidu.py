# -*- coding: utf-8 -*-
import requests
import threading
import hashlib
import os
from bs4 import BeautifulSoup

class Baidu(object):
    def __init__(self):
        self.base_url = 'https://www.baidu.com'
        self.resource = 'baidu'
        self.category = ''

    def get_file_name(self):
        return os.path.join(self.resource, self.category, self.id)

class BaiduNews(Baidu):
    def __init__(self, query=None):
        super(BaiduNews, self).__init__()
        self.category = 'news'
        self.base_url = 'https://news.baidu.com'
        self.query = query
        if query:
            self.id = hashlib.sha1(query.encode('utf-8')).hexdigest()
        else:
            self.id = 'top'

    def get_news(self):
        news = []
        if not self.query:
            score = 6
            resp = requests.get(self.base_url)
            resp.raise_for_status()
            data = BeautifulSoup(resp.text, 'html.parser')
            for title in data.find(id='pane-news').find_all('a'):
                news.append((title.text + ' ') * score)
                if len(news) % 5 == 0 and score > 1:
                    score -= 1
        return news

    def get_content(self):
        return ''.join(self.get_news())

if __name__ == '__main__':
    bn = BaiduNews()
    print(bn.get_content())
