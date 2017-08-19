from cloudatlas import CloudAtlas
from flask import Flask
from flask import request
from flask import send_file
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/wordcloud",  methods=["GET"])
def get_wordcloud():
    query = request.args.get('q', '')
    ca = CloudAtlas(query)
    with open(ca.do_query()) as f:
        return send_file(f, mimetype='image/png')
