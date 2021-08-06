from flask import Flask, request, Response
from flask_cors import CORS
# from utils.apscheduler import run_schd

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/',methods=["GET","POST"])
def hello_world():
  if request.method == "GET":
    client = request.remote_addr
    return {"message": "ok","client":client}
  elif request.method == "POST":
    return {'message':'ok'}

@app.errorhandler(404)
def handle_404_error(err):
  return {"message":f'{err}',"code":404}
  
@app.errorhandler(405)
def handle_405_error(err):
  return {"message":f'{err}',"code":405}

@app.errorhandler(500)
def handle_500_error(err):
  return {"message":f'{err}',"code":500}

from routers.anls_router import *
from routers.mng_router import *
from routers.mvt_router import *

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,debug=True)