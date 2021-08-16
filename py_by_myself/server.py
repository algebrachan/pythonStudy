from flask import Flask
import time

app = Flask(__name__)

@app.route('/bobo')
def index_bobo():
  time.sleep(2)
  return 'hello bobo'

@app.route('/jay')
def index_javy():
  time.sleep(2)
  return 'hello jay'

@app.route('/tom')
def index_tom():
  time.sleep(2)
  return 'hello tom'

if __name__ == '__main__':
    app.run()
    