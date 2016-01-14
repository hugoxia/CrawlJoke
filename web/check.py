import requests
import json

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/next')
def _next():
    test = request.form['etag']
    print(test)


@app.route('/delete/<url>/<etag>')
def _delete(url, etag):
    headers = {'content-type': 'application/json', 'If-Match': etag}
    requests.delete('http://cold.tarsbot.com/' + url,
                    headers=headers,
                    allow_redirects=False)


# @app.route('/test', methods=['POST'])
# def check_joke():
#     answer = request.form['answer']
#     author = request.form['author']
#     via = request.form['via']
#     via_url = request.form['via_url']
#     content = request.form['edit_text']
#     folder = request.form['folder']
#     etag = request.form['etag']
#     upload = {'_items': []}
#     for i in [answer, author, via, via_url, content]:
#         if i is not None:
#             upload['_items'].append(i)
#         else:
#             pass
#     headers = {'content-type': 'application/json', 'If-Match': etag}
#     requests.post('http://cold.tarsbot.com/' + folder + '/',
#                   data=json.dumps(upload),
#                   headers=headers,
#                   allow_redirects=False)
#     return 'OK'


@app.route('/<via_name>', methods=['GET', 'POST'])
def check(via_name):
    if request.method == 'GET':
        r = requests.get('http://cold.tarsbot.com/' + via_name)
        try:
            _id = eval(r.text)['_items'][0]['_id']
        except KeyError:
            _id = None
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
        try:
            etag = eval(r.text)['_items'][0]['_etag']
        except KeyError:
            etag = None
        try:
            total = eval(r.text)['_meta']['total']
        except KeyError:
            total = None
        # api_url is the url of current joke
        try:
            api_url = eval(r.text)['_link']['self']['href']
        except KeyError:
            api_url = None
        return render_template('check.html',
                               author=author,
                               via=via,
                               id=_id,
                               via_url=via_url,
                               api_url=api_url,
                               content=content,
                               answer=answer,
                               etag=etag,
                               total=total
                               )
    elif request.method == 'POST':
        _id = request.form['id']
        answer = request.form['answer']
        author = request.form['author']
        via = request.form['via']
        via_url = request.form['via_url']
        content = request.form['edit_text']
        folder = request.form['folder']
        etag = request.form['etag']
        upload = {'_items': []}
        print(_id, answer, author, via, via_url, content, etag)
        for i in [answer, author, via, via_url, content]:
            if i is not None:
                upload['_items'].append(i)
            else:
                pass
        headers = {'content-type': 'application/json', 'If-Match': etag}
        print('http://cold.tarsbot.com/' + folder + '/')
        print(upload)
        # requests.post('http://cold.tarsbot.com/' + folder + '/',
        #               data=json.dumps(upload),
        #               headers=headers,
        #               allow_redirects=False)
        return 'OK'


if __name__ == '__main__':
    app.run(debug=True, port=9999)
