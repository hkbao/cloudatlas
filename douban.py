import requests
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
            self.id = str(id)
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
        resp = requests.get(self.api_url + "/movie/subject/" + self.id)
        resp.raise_for_status()
        return resp.json()

    def get_comments(self):
        comments = []
        next_page = self.url + "/comments"
        for i in range(10):
            resp = requests.get(next_page)
            if resp.status_code != 200:
                break
            data = BeautifulSoup(resp.text, "html.parser")
            np_button = data.find("div", id="paginator").find("a", class_="next")
            for comment in data.find_all("div", class_="comment"):
                comments.append(comment.p.text.strip())
            if np_button:
                next_page = self.url + "/comments" + np_button["href"]
            else:
                break
        return comments

    def get_content(self):
        return "".join(self.get_comments())
