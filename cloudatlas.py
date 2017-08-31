# -*- coding: utf-8 -*-
import os
import time
import json
import hashlib
import jieba.analyse
from cache import cache
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFont

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

script_path = os.path.dirname(os.path.realpath(__file__))

class CloudAtlas(object):
    def __init__(self, obj, rebuild=False, watermark=None):
        self.obj = obj
        self.rebuild = rebuild
        self.watermark = json.loads(watermark) if watermark else None
        self.font = os.path.join(script_path, 'resources', 'fonts', 'HiraginoW3.otf')

    def get_keywords(self, content):
        # First, eliminate stopwords
        # Use jieba to cut words
        if content == '':
            return {'你搜索的内容太小众了，没找到任何信息...': 1}
        tags = jieba.analyse.extract_tags(content, withWeight=True, topK=200)
        return dict(tags)

    def get_keyword_cloud(self, content):
        wc = WordCloud(font_path=self.font, \
            width=680, height=400, background_color='white', max_font_size=150)
        wc = wc.fit_words(self.get_keywords(content))
        data = BytesIO()
        wc.to_image().save(data, format='png')
        return data

    def get_cloud_img_url(self):
        file_name = self.obj.get_file_name() + '.png'
        if self.rebuild or not cache.exists(file_name, 604800):
            img = self.get_keyword_cloud(self.obj.get_content())
            cache.put(file_name, img)
       	if self.watermark:
            file_name = self.get_watermark_img()
        return cache.get_url(file_name)

    def get_keyword_data(self):
        file_name = self.obj.get_file_name() + '.txt'
        if self.rebuild or not cache.exists(file_name, 3600):
            data = json.dumps(self.get_keywords(self.obj.get_content()))
            cache.put(file_name, data, obj_type='txt')
        else:
            data = cache.get(file_name).read()
        return data

    def get_watermark_img(self):
        file_name = self.obj.get_file_name() + '.png'
        file_name_wm = self.obj.get_file_name() + '_wm.png'
        img = self.add_watermark(file_name, file_name_wm)
        cache.put(file_name_wm, img)
        return file_name_wm

    def add_watermark(self, img_path, cache_file_wm):
        font = self.font
        baseim = Image.open(os.path.join(script_path, 'resources', 'images', 'watermark.png'))
        wordim = Image.open(cache.get(img_path))
        textim = Image.new('RGB', (680, 180), (255, 255, 255))
        textim_dr = ImageDraw.Draw(textim)
        textim_dr.text((10, 10), self.watermark.get('title', ''), font=ImageFont.truetype(font, 36), fill='#000000')
        textim_dr.text((10, 70), self.watermark.get('rating', ''), font=ImageFont.truetype(font, 18), fill='#000000')
        textim_dr.text((10, 160), u'以下是根据豆瓣短评生成的关键词云图', font=ImageFont.truetype(font, 14), fill='#0f0f0f')
        baseim.paste(wordim, (10, 200, 690, 600))
        baseim.paste(textim, (10, 10, 690, 190))
        data = BytesIO()
        baseim.save(data, format='png')
        return data

if __name__ == '__main__':
    pass
    #movie = douban.DoubanBook('27068494')
    #wc = CloudAtlas(movie, watermark=True)
    #wc.get_cloud_img()
