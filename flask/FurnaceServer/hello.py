from flask import Flask,request,views
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/',methods=["GET"])
def hello_world(name:str='',age:int=0):
    
    return name+str(age)

@app.route("/index",methods=["POST"])
def index_test():
    # data = json.loads(request.get_data(as_text=True)) 
    data = request.get_json()
    print(type(data))
    return data

class IndexView(views.MethodView):
      methods = ['GET']
      def get(self):
          return 'Index.GET'
 
      def post(self):
          return 'Index.POST'
 
 
app.add_url_rule('/test', view_func=IndexView.as_view(name='test'))

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,debug=True)