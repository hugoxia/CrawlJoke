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


@app.route('/next/<via_name>/<id>')
def _next(via_name, id):
    if via_name == 'fml' or via_name == 'joke' or via_name == 'dirty':
        return '暂不支持'
    else:
        r = requests.get('http://cold.tarsbot.com/' + via_name + '/' + id)
        t = requests.get('http://cold.tarsbot.com/' + via_name)

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
            total = json.JSONDecoder().decode(t.text)['_meta']['total']
        except (KeyError, IndexError):
            total = None
        # api_url is the url of current joke
        try:
            api_url = json.JSONDecoder().decode(r.text)['_link']['self']['href']
        except (KeyError, IndexError):
            api_url = None
        next_url = via_name + '/' + hex(int(id, 16) + int('1', 16))[2:]
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
        if _id:
            next_url = via_name + '/' + hex(int(_id, 16) + int('1', 16))[2:]
        else:
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
                               via_name=via_name
                               )
    elif request.method == 'POST':
        post_dict = {}
        _id = request.form['id']
        answer = request.form['answer']
        author = request.form['author']
        via = request.form['via']
        via_url = request.form['via_url']
        content = request.form['edit_text']
        folder = request.form['folder']
        etag = request.form['etag']
        if answer != 'None':
            post_dict['answer'] = answer
        if author != 'None':
            post_dict['author'] = author
        if via != 'None':
            post_dict['via'] = via
        if via_url != 'None':
            post_dict['via_url'] = via_url
        if content != 'None':
            post_dict['content'] = content
        headers = {'content-type': 'application/json', 'If-Match': etag}
        requests.post('http://cold.tarsbot.com/' + folder + '/',
                      data=json.dumps(post_dict),
                      headers=headers,
                      allow_redirects=False)
        requests.delete('http://cold.tarsbot.com/' + via_name + '/' + _id,
                        headers=headers,
                        allow_redirects=False)
        return 'Modify OK'
    else:
        return '404'


# @app.route('/<via_name>/<_id>', methods=['PUT', 'PATCH'])
# def check(via_name, _id):
#     r = requests.get('http://cold.tarsbot.com/' + via_name + '/' + _id)
#     try:
#         etag = json.JSONDecoder().decode(r.text)['_etag']
#     except (KeyError, IndexError):
#         etag = None
#     if request.method == 'PUT':
#         return 'TEST PUT'
#     elif request.method == 'PATCH':
#         headers = {'content-type': 'application/json', 'If-Match': etag}
#         requests.patch('http://cold.tarsbot.com/' + via_name + '/' + _id,
#                        headers=headers,
#                        allow_redirects=False)
#         return 'TEST DELETE'
#     else:
#         return 'TEST'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
