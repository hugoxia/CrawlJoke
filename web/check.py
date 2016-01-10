from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def select():
    return render_template('index.html')


@app.route('/<via>')
def check(via):
    author = ''
    via_url = ''
    return render_template('check.html',
                           author=author,
                           via=via,
                           via_url=via_url
                           )

if __name__ == '__main__':
    app.run(debug=True)