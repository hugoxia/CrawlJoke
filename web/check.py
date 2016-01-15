import requests
import json
import re

from flask import Flask, redirect
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/next/<url>')
def _next(url):
    r = requests.get('http://cold.tarsbot.com/' + url)
    try:
        _id = json.JSONDecoder().decode(r.text)['_id']
    except (KeyError, IndexError):
        _id = None
    try:
        author = json.JSONDecoder().decode(r.text)['author']
    except (KeyError, IndexError):
        author = None
    try:
        via = json.JSONDecoder().decode(r.text)['via']
    except (KeyError, IndexError):
        via = None
    try:
        via_url = json.JSONDecoder().decode(r.text)['via_url']
    except (KeyError, IndexError):
        via_url = None
    try:
        content = json.JSONDecoder().decode(r.text)['content']
    except (KeyError, IndexError):
        content = None
    try:
        answer = json.JSONDecoder().decode(r.text)['answer']
    except (KeyError, IndexError):
        answer = None
    try:
        etag = json.JSONDecoder().decode(r.text)['_etag']
    except (KeyError, IndexError):
        etag = None
    try:
        total = json.JSONDecoder().decode(r.text)['_meta']['total']
    except (KeyError, IndexError):
        total = None
    # api_url is the url of current joke
    try:
        api_url = json.JSONDecoder().decode(r.text)['_link']['self']['href']
    except (KeyError, IndexError):
        api_url = None
    try:
        next_url = json.JSONDecoder().decode(r.text)['_items'][1]['_link']['self']['href']
    except (KeyError, IndexError):
        next_url = None
    return render_template('check.html',
                           author=author,
                           via=via,
                           id=_id,
                           via_url=via_url,
                           api_url=api_url,
                           next_url=next_url,
                           content=content,
                           answer=answer,
                           etag=etag,
                           total=total,
                           via_name=re.split(r'/', url)[0]
                           )


@app.route('/delete/<via_name>/<_id>/<etag>')
def _delete(via_name, _id, etag):
    headers = {'content-type': 'application/json', 'If-Match': etag}
    requests.delete('http://cold.tarsbot.com/' + via_name + '/' + _id,
                    headers=headers,
                    allow_redirects=False)
    return redirect("/" + via_name, code=302)


@app.route('/<via_name>', methods=['GET', 'POST'])
def check(via_name):
    if request.method == 'GET':
        r = requests.get('http://cold.tarsbot.com/' + via_name)
        try:
            _id = json.JSONDecoder().decode(r.text)['_items'][0]['_id']
        except (KeyError, IndexError):
            _id = None
        try:
            author = json.JSONDecoder().decode(r.text)['_items'][0]['author']
        except (KeyError, IndexError):
            author = None
        try:
            via = json.JSONDecoder().decode(r.text)['_items'][0]['via']
        except (KeyError, IndexError):
            via = None
        try:
            via_url = json.JSONDecoder().decode(r.text)['_items'][0]['via_url']
        except (KeyError, IndexError):
            via_url = None
        try:
            content = json.JSONDecoder().decode(r.text)['_items'][0]['content']
        except (KeyError, IndexError):
            content = None
        try:
            answer = json.JSONDecoder().decode(r.text)['_items'][0]['answer']
        except (KeyError, IndexError):
            answer = None
        try:
            etag = json.JSONDecoder().decode(r.text)['_items'][0]['_etag']
        except (KeyError, IndexError):
            etag = None
        try:
            total = json.JSONDecoder().decode(r.text)['_meta']['total']
        except (KeyError, IndexError):
            total = None
        # api_url is the url of current joke
        try:
            api_url = json.JSONDecoder().decode(r.text)['_link']['self']['href']
        except (KeyError, IndexError):
            api_url = None
        try:
            next_url = json.JSONDecoder().decode(r.text)['_items'][1]['_link']
        except (KeyError, IndexError):
            next_url = None
        print(type(next_url))
        return render_template('check.html',
                               author=author,
                               via=via,
                               id=_id,
                               via_url=via_url,
                               api_url=api_url,
                               next_url=next_url,
                               content=content,
                               answer=answer,
                               etag=etag,
                               total=total,
                               via_name=via_name
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
        # print(request.form)
        # upload = {'_items': []}
        # for i in [answer, author, via, via_url, content]:
        #     if i != 'None':
        #         upload['_items'].append(i)
        #     else:
        #         pass
        print(etag)
        headers = {'content-type': 'application/json', 'If-Match': etag}
        requests.post('http://cold.tarsbot.com/' + folder + '/',
                      data=json.dumps({'content': content, 'via': via, 'via_url': via_url}),
                      headers=headers,
                      allow_redirects=False)
        requests.delete('http://cold.tarsbot.com/' + via_name + '/' + _id,
                        headers=headers,
                        allow_redirects=False)
        return 'Modify OK'


# @app.route('/<via_name>/<_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
# def check(via_name, _id):
#     if request.method == 'GET':
#         pass
#         return 'TEST GET'
#     elif request.method == 'PUT':
#         pass
#         return 'TEST PUT'
#     elif request.method == 'PATCH':
#         pass
#         return 'TEST PATCH'
#     elif request.method == 'DELETE':
#         etag = ''
#         headers = {'content-type': 'application/json', 'If-Match': etag}
#         requests.delete('http://cold.tarsbot.com/' + via_name + '/' + _id,
#                         headers=headers,
#                         allow_redirects=False)
#         pass
#         return 'TEST DELETE'
#     else:
#         pass
#         return 'TEST'


if __name__ == '__main__':
    app.run(debug=True, port=9999)
