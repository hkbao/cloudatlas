import os
import time
import hashlib
import jieba.analyse
from wordcloud import WordCloud

try:
    import matplotlib.pyplot as plt
except:
    import matplotlib
    matplotlib.use("agg", warn=False, force=True)
    from matplotlib import pyplot as plt

try:
    import configparser
    config = configparser.ConfigParser()
    config.read("config.conf")
    cache_path = config["cache_path"]
except Exception:
    cache_path = "/home/ec2-user/cached-files"
finally:
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

class CloudAtlas(object):
    def __init__(self, obj, rebuild=False):
        self.obj = obj
        self.rebuild = rebuild

    def get_keywords(self, content):
        # First, eliminate stopwords
        # Use jieba to cut words
        if content == "":
            return {"你搜索的内容太小众了，没找到任何信息...": 1}
        tags = jieba.analyse.extract_tags(content, withWeight=True, topK=200)
        return dict(tags)

    def get_keyword_cloud(self, content, filepath):
        wc = WordCloud(font_path=get_script_path() + "/yahei.ttf", \
            width=680, height=400, background_color="white", max_font_size=150)
        wc = wc.fit_words(self.get_keywords(content))
        plt.imshow(wc)
        plt.axis("off")
        plt.figure()
        wc.to_file(filepath)

    def get_cloud_img(self):
        id_sha1     = hashlib.sha1(self.obj.id.encode("utf-8")).hexdigest()
        second_path = os.path.join(cache_path, self.obj.resource, id_sha1[0:2])
        cache_file  = os.path.join(second_path, id_sha1 + ".png")
        if self.rebuild or not self.is_recent_file(cache_file):
            if not os.path.exists(second_path):
                os.makedirs(second_path)
            self.get_keyword_cloud(self.obj.get_content(), cache_file)
        return cache_file

    def is_recent_file(self, filepath):
        # if file is modified within 7 days, it's a recent file
        if os.path.exists(filepath):
            return True
        else:
            return False

if __name__ == "__main__":
    pass
