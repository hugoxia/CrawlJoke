from flask import Flask
from flask import render_template
from pymongo import MongoClient
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.crandom
collection = db.pengfu
mongo = PyMongo(app)


@app.route('/')
def select():
    return render_template('index.html')


@app.route('/<via>')
def check(via):
    author = ''
    via_url = ''
    content = collection.find_one({"via": "pengfuwang"})[u'content']
    return render_template('check.html',
                           author=author,
                           via=via,
                           via_url=via_url,
                           content=content
                           )

if __name__ == '__main__':
    app.run(debug=True)