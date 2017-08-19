import os
import time
import hashlib
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from douban import DoubanMovie

try:
    import configparser
    config = configparser.ConfigParser()
    config.read("config.conf")
    cache_path = config["cache_path"]
except Exception:
    cache_path = "./cached-files"
finally:
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

class CloudAtlas(object):
    def __init__(self, query):
        self.query = query

    def get_keywords(self, content):
        # First, eliminate stopwords
        # Use jieba to cut words
        tags = jieba.analyse.extract_tags(content, withWeight=True, topK=200)
        return dict(tags)

    def get_keyword_cloud(self, content, filepath):
        wc = WordCloud(font_path="yahei.ttf", width=680, height=400, background_color="white", max_font_size=150)
        wc = wc.fit_words(self.get_keywords(content))
        plt.imshow(wc)
        plt.axis("off")
        plt.figure()
        wc.to_file(filepath)

    def do_query(self):
        query_sha1  = hashlib.sha1(self.query).hexdigest()
        second_path = os.path.join(cache_path, query_sha1[0:2])
        cache_file  = os.path.join(second_path, query_sha1 + ".png")
        if not self.is_recent_file(cache_file):
            if not os.path.exists(second_path):
                os.mkdir(second_path)
            obj = self.triage_query()
            self.get_keyword_cloud(obj.get_content(), cache_file)
        return cache_file

    def triage_query(self):
        # do something to triage a query, so that we know which object to new
        return DoubanMovie(self.query)

    def is_recent_file(self, filepath):
        # if file is modified within 7 days, it's a recent file
        if os.path.exists(filepath) and time.time() - os.path.getmtime(filepath) < 604800:
            return True
        else:
            return False

if __name__ == "__main__":
    ca = CloudAtlas(u"嫌疑人x的献身")
    ca.do_query()
