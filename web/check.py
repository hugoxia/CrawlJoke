import requests
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<via>')
def check(via):
    r = requests.get('http://cold.tarsbot.com/' + via)
    try:
        author = eval(r.text)['_items'][0]['author']
    except KeyError:
        author = None
    try:
        via = eval(r.text)['_items'][0]['via']
    except KeyError:
        via = None
    try:
        via_url = eval(r.text)['_items'][0]['via_url']
    except KeyError:
        via_url = None
    try:
        content = eval(r.text)['_items'][0]['content']
    except KeyError:
        content = None
    try:
        answer = eval(r.text)['_items'][0]['answer']
    except KeyError:
        answer = None
    return render_template('check.html',
                           author=author,
                           via=via,
                           via_url=via_url,
                           content=content,
                           answer=answer
                           )


if __name__ == '__main__':
    app.run(debug=True)
