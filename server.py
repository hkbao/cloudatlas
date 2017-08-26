from cloudatlas import CloudAtlas
from wechat.handler import wechat_auth, handle_msg
from douban import DoubanMovie, DoubanBook, DoubanMusic
from flask import Flask
from flask import json
from flask import request
from flask import send_file
from flask import render_template
app = Flask(__name__)

@app.route("/app", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        if wechat_auth(request):
            return request.args.get("echostr", "")
        else:
            return ""
    if request.method == "POST":
        if wechat_auth(request):
            return handle_msg(request.data)
        else:
            abort(401)

@app.route("/app/wordcloud", methods=["GET"])
def get_wordcloud():
    qtype  = request.args.get("t", "movie")
    query = request.args.get("q", "")
    try:
        if qtype == "movie":
            obj = DoubanMovie(query)
        elif qtype == "book":
            obj = DoubanBook(query)
        elif qtype == "music":
            obj = DoubanMusic(query)
        else:
            raise Exception("Unknown type: " + type)
        ca = CloudAtlas(obj, request.args.get("refresh", False), request.args.get("watermark", False))
    except Exception as e:
        return str(e)
    else:
        return send_file(ca.get_cloud_img(), mimetype="image/png")

@app.route("/app/movie/<name>", methods=["GET"])
def get_movie(name):
    try:
        movie = DoubanMovie(name=name)
        basic_info = movie.get_basic_info()
        return render_template('movie_info.html', **basic_info)
    except Exception as e:
        return str(e)

#@app.route("/app/movie2/<name>", methods=["GET"])
#def get_movie2(name):
#    try:
#        movie = DoubanMovie(name=name)
#        if request.args.get("accept") == "json":
#            return json.dumps(movie.get_basic_info())
#        else:
#            return render_template('movie_info2.html', **movie.__dict__)
#    except Exception as e:
#        return str(e)
