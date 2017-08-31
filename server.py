from cloudatlas import CloudAtlas
from wechat.handler import wechat_auth, handle_msg
from douban import DoubanMovie, DoubanBook, DoubanMusic
from baidu import BaiduNews
from config import env
from flask import Flask
from flask import json
from flask import request
from flask import redirect
from flask import send_file
from flask import render_template
import os.path
app = Flask(__name__)


@app.route('/app', methods=['GET'])
def main():
    return 'Hello! Welcome to Ted\'s APP'

@app.route('/app/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        if wechat_auth(request):
            return request.args.get('echostr', '')
        else:
            return ''
    if request.method == 'POST':
        if wechat_auth(request):
            return handle_msg(request.data)
        else:
            abort(401)

@app.route('/app/wordcloud', methods=['GET'])
def get_wordcloud():
    qtype  = request.args.get('t', 'movie')
    query = request.args.get('q', '')
    try:
        if qtype == 'movie':
            obj = DoubanMovie(query)
        elif qtype == 'book':
            obj = DoubanBook(query)
        elif qtype == 'music':
            obj = DoubanMusic(query)
        elif qtype == 'news':
            obj = BaiduNews(query)
        else:
            raise Exception('Unknown type: ' + qtype)
        ca = CloudAtlas(obj, request.args.get('refresh', False), request.args.get('watermark', False))
    except Exception as e:
        return str(e)
    else:
        if env == 'production':
            return redirect(ca.get_cloud_img_url(), code=302)
        else:
            return send_file(ca.get_cloud_img_url(), mimetype='image/png')

@app.route('/app/kwdata', methods=['GET'])
def get_kwdata():
    qtype  = request.args.get('t', 'news')
    query = request.args.get('q', None)
    try:
        if qtype == 'news':
            obj = BaiduNews(query)
        else:
            raise Exception('Unknown type: ' + qtype)
        ca = CloudAtlas(obj, request.args.get('refresh', False), request.args.get('watermark', False))
    except Exception as e:
        return str(e)
    else:
        return ca.get_keyword_data()

@app.route('/app/movie/<name>', methods=['GET'])
def get_movie(name):
    try:
        movie = DoubanMovie(name=name)
        basic_info = movie.get_basic_info()
        return render_template('movie_info.html', **basic_info)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    pass
