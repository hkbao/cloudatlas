# -*- coding: utf-8 -*-
import requests
import threading
from bs4 import BeautifulSoup

class Douban(object):
    def __init__(self):
        self.base_url = "https://www.douban.com"
        self.api_url  = "https://api.douban.com/v2"
        self.resource = ""

    def search_resource(self, name):
        resp = requests.get(self.base_url + "/j/subject_suggest", params={"q": name})
        resp.raise_for_status()
        data = resp.json()
        if len(data) > 0:
            self.title = data[0]["title"]
            self.id = data[0]["id"]
            self.url = self.base_url + "/subject/" + self.id
        else:
            raise Exception("%s resource not found according to the keyword \"%s\"" % (self.resource, name))

    def get_comments(self):
        comments = []
        threads = []
        def get_comment_page(url):
            resp = requests.get(url)
            if resp.status_code != 200:
                return
            data = BeautifulSoup(resp.text, "html.parser")
            for comment in data.find_all("div", class_="comment"):
                comments.append(comment.p.text.strip())
        for i in range(10):
            page_url = self.get_comment_page_url(i)
            threads.append(threading.Thread(target=get_comment_page,args=(page_url,)))
            threads[-1].start()
        for t in threads:
            t.join()
        return set(comments)

    def get_content(self):
        return "".join(self.get_comments())

class DoubanMovie(Douban):
    def __init__(self, name):
        super(DoubanMovie, self).__init__()
        self.base_url = "https://movie.douban.com"
        self.resource = "movie"
        if name.isdigit() and int(name) > 10000:
            self.id = str(name)
            self.url = self.base_url + "/subject/" + self.id
        else:
            self.search_resource(name)

    def get_basic_info(self):
        resp = requests.get(self.api_url + "/movie/" + self.id)
        resp.raise_for_status()
        info = resp.json()
        info["mid"] = self.id
        info["image"] = info["image"].replace("/ipst/", "/mpst/")
        for key in info["attrs"]:
            info["attrs"][key] = u"/".join([attr.split(" ")[0] for attr in info["attrs"][key][0:5]])
        info["title_str"] = info["title"] + u" (%s)" % info["attrs"]["year"]
        info["attrs_str"] = u"%s (导演)/%s" % (info["attrs"]["director"], "/".join([info["attrs"]["cast"],\
            info["attrs"]["movie_type"], info["attrs"]["country"], info["attrs"]["movie_duration"]]))
        info["rating_str"] = u"豆瓣评分: %s (共 %d 人评价)" % (info["rating"]["average"], info["rating"]["numRaters"])
        return info

    def get_comment_page_url(self, page_num):
        return self.url + "/comments?start=%d&limit=20&sort=new_score&status=P" % (page_num * 20)

class DoubanBook(Douban):
    def __init__(self, name):
        super(DoubanBook, self).__init__()
        self.base_url = "https://book.douban.com"
        self.resource = "book"
        if name.isdigit() and int(name) > 10000:
            self.id = str(name)
            self.url = self.base_url + "/subject/" + self.id
        else:
            self.search_resource(name)

    def get_basic_info(self):
        resp = requests.get(self.api_url + "/book/" + self.id)
        resp.raise_for_status()
        info = resp.json()
        info["title_str"] = info["title"] + u" (%s)" % info.get("pubdate")
        info["attrs_str"] = u"%s (作者)/%s/%s" % ("/".join(info["author"]), info["publisher"], \
            info.get("price", ""))
        info["rating_str"] = u"豆瓣评分: %s (共 %d 人评价)" % (info["rating"]["average"], info["rating"]["numRaters"])
        return info

    def get_comment_page_url(self, page_num):
        return self.url + "/comments/hot?p=%d" % (page_num + 1)

class DoubanMusic(Douban):
    def __init__(self, name):
        super(DoubanMusic, self).__init__()
        self.base_url = "https://music.douban.com"
        self.resource = "music"
        if name.isdigit() and int(name) > 10000:
            self.id = str(name)
            self.url = self.base_url + "/subject/" + self.id
        else:
            self.search_resource(name)

    def get_basic_info(self):
        resp = requests.get(self.api_url + "/music/" + self.id)
        resp.raise_for_status()
        info = resp.json()
        info["title_str"] = info["title"]
        info["attrs_str"] = u"%s (音乐人)/%s/%s" % (info["author"][0]["name"], info["attrs"]["version"][0],\
            info["attrs"]["publisher"][0])
        info["rating_str"] = u"豆瓣评分: %s (共 %d 人评价)" % (info["rating"]["average"], info["rating"]["numRaters"])
        return info

    def get_comment_page_url(self, page_num):
        return self.url + "/comments/hot?p=%d" % (page_num + 1)

if __name__ == "__main__":
    movie = DoubanMovie("24753810")
    print(movie.get_basic_info())
    print(movie.get_content())

    book = DoubanBook("2567698")
    print(book.get_basic_info())
    print(book.get_content())

    music = DoubanMusic("27086571")
    print(music.get_basic_info())
    print(music.get_content())
