__DEBUG = True

from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def greeting():
    return 'Welcome, flask is COOL!'

@app.route('/test/hello/')
@app.route('/test/hello/<username>')
def hello(username=None):
    #return 'Hello %s' % username
    return render_template('hello.html', name=username)


if __name__ == '__main__':
    if __DEBUG:
        app.run(debug=True)
    else :
        app.run(host='0.0.0.0')
