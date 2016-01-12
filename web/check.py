from flask import Flask
from flask import render_template
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def select():
    return render_template('index.html')


@app.route('/<via>')
def check(via):
    author = ''
    via_url = ''
    test = mongo.db.via.find()
    content = test['content']
    return render_template('check.html',
                           author=author,
                           via=via,
                           via_url=via_url,
                           content=content
                           )

if __name__ == '__main__':
    app.run(debug=True)