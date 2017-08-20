from cloudatlas import CloudAtlas
from douban import DoubanMovie
from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
app = Flask(__name__)

@app.route("/app")
def hello():
    return "Hello World!!"

@app.route("/app/wordcloud",  methods=["GET"])
def get_wordcloud():
    wtype  = request.args.get("t", "movie")
    query = request.args.get("q", "")
    try:
        if wtype == "movie":
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
