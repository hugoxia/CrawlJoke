from flask import Flask
from flask import render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.crandom
collection = db.pengfu


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<via>')
def check(via):
    author = ''
    via_url = ''
    content_list = []
    contents = collection.find({"via": "pengfu"}, limit=10)
    for content in contents:
        content_list.append(content)
    return render_template('check.html',
                           author=author,
                           via=via,
                           via_url=via_url,
                           content=content_list[0][u'content']
                           )

if __name__ == '__main__':
    app.run(debug=True)
