from cloudatlas import CloudAtlas
from wechathandler import wechat_echo
from douban import DoubanMovie
from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
app = Flask(__name__)

@app.route("/app")
def main():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce     = request.args.get("nonce", "")
    echostr   = request.args.get("echostr", "")
    return wechat_echo(signature, timestamp, nonce, echostr)

@app.route("/app/wordcloud",  methods=["GET"])
def get_wordcloud():
    qtype  = request.args.get("t", "movie")
    query = request.args.get("q", "")
    try:
        if qtype == "movie":
            obj = DoubanMovie(query)
        else:
            raise Exception("Unknown type: " + type)
        ca = CloudAtlas(obj)
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
