# -*- coding: utf-8 -*-
import os
import time
import hashlib
import jieba.analyse
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFont

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
    def __init__(self, obj, rebuild=False, watermark=False):
        self.obj = obj
        self.rebuild = rebuild
        self.watermark = watermark

    def get_keywords(self, content):
        # First, eliminate stopwords
        # Use jieba to cut words
        if content == "":
            return {"你搜索的内容太小众了，没找到任何信息...": 1}
        tags = jieba.analyse.extract_tags(content, withWeight=True, topK=200)
        return dict(tags)

    def get_keyword_cloud(self, content, filepath):
        wc = WordCloud(font_path=os.path.join(get_script_path(), "yahei.ttf"), \
            width=680, height=400, background_color="white", max_font_size=150)
        wc = wc.fit_words(self.get_keywords(content))
        wc.to_file(filepath)

    def get_cloud_img(self):
        id_sha1     = hashlib.sha1(self.obj.id.encode("utf-8")).hexdigest()
        second_path = os.path.join(cache_path, self.obj.resource, id_sha1[0:2])
        cache_file  = os.path.join(second_path, id_sha1 + ".png")
        if self.rebuild or not self.is_recent_file(cache_file):
            if not os.path.exists(second_path):
                os.makedirs(second_path)
            self.get_keyword_cloud(self.obj.get_content(), cache_file)
        if self.watermark:
            cache_file_wm = cache_file.replace(".png", '_wm.png')
            if self.is_recent_file(cache_file_wm, days=7):
                cache_file = cache_file_wm
            else:
                cache_file = self.add_watermark(cache_file, cache_file_wm)
        return cache_file

    def add_watermark(self, img_path, cache_file_wm):
        info = self.obj.get_basic_info()
        font = os.path.join(get_script_path(), "yahei.ttf")
        baseim = Image.open(os.path.join(get_script_path(), "images", "watermark.png"))
        wordim = Image.open(img_path)
        textim = Image.new('RGB', (680, 180), (255, 255, 255))
        textim_dr = ImageDraw.Draw(textim)
        textim_dr.text((10, 10), info.get("title_str", ""), font=ImageFont.truetype(font, 36), fill="#000000")
        textim_dr.text((10, 70), info.get("rating_str", ""), font=ImageFont.truetype(font, 18), fill="#000000")
        textim_dr.text((10, 100), info.get("attrs_str", ""), font=ImageFont.truetype(font, 18), fill="#0f0f0f")
        textim_dr.text((10, 160), u"以下是根据豆瓣短评生成的关键词云图", font=ImageFont.truetype(font, 14), fill="#0f0f0f")
        baseim.paste(wordim, (10, 200, 690, 600))
        baseim.paste(textim, (10, 10, 690, 190))
        baseim.save(cache_file_wm, 'PNG')
        return cache_file_wm

    def is_recent_file(self, filepath, days=365):
        # if file is modified within 7 days, it's a recent file
        if os.path.exists(filepath) and \
            (time.time() - os.path.getmtime(filepath) < (86400 * days)):
            return True
        else:
            return False

if __name__ == "__main__":
    pass
    #movie = douban.DoubanBook("27068494")
    #wc = CloudAtlas(movie, watermark=True)
    #wc.get_cloud_img()
