
from bottle import route, run
p = {1:2}
@route('/hello/<no>')
def hello(no):
    return no

run(host='localhost', port=3000, debug=True)