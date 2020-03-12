from flask import Flask
from func import *

server = Flask('server')

@server.route('/logincode')
def logincode():
    


if __name__ == '__main__':
    server.run(debug=True)

