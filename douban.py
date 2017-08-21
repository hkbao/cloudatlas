import requests
import threading
from bs4 import BeautifulSoup

class Douban(object):
    def __init__(self):
        self.base_url = "https://www.douban.com"
        self.api_url = "https://api.douban.com/v2"

class DoubanMovie(Douban):
    def __init__(self, name):
        super(DoubanMovie, self).__init__()
        self.base_url = "https://movie.douban.com"
        if name.isdigit() and int(name) > 100000:
            self.id = str(name)
            self.url = self.base_url + "/subject/" + self.id
        else:
            self.search_movie(name)

    def search_movie(self, name):
        resp = requests.get(self.base_url + "/j/subject_suggest", params={"q": name})
        resp.raise_for_status()
        data = resp.json()
        if len(data) > 0:
            self.title = data[0]["title"]
            self.id = data[0]["id"]
            self.url = self.base_url + "/subject/" + self.id
        else:
            raise Exception("Movie not found according to the keyword \"%s\"" % name)

    def get_basic_info(self):
        resp = requests.get(self.api_url + "/movie/" + self.id)
        resp.raise_for_status()
        info = resp.json()
        info["mid"] = self.id
        info["image"] = info["image"].replace("/ipst/", "/mpst/")
        for key in info["attrs"]:
            info["attrs"][key] = "/".join([attr.split(" ")[0] for attr in info["attrs"][key][0:5]])
        return info

    def get_comments(self):
        comments = []
        threads = []
        def get_comment_page(url):
            resp = requests.get(url)
            if resp.status_code != 200:
                print("oops %d" % resp.status_code)
                return
            data = BeautifulSoup(resp.text, "html.parser")
            for comment in data.find_all("div", class_="comment"):
                comments.append(comment.p.text.strip())
        for i in range(10):
            page_url = self.url + "/comments?start=%d&limit=20&sort=new_score&status=P" % (i * 20)
            threads.append(threading.Thread(target=get_comment_page,args=(page_url,)))
            threads[-1].start()
        for t in threads:
            t.join()
        return set(comments)

    def get_content(self):
        return "".join(self.get_comments())

if __name__ == "__main__":
    movie = DoubanMovie("ted2")
    print(movie.get_content())
