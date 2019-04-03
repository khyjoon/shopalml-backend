from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson.json_util import dumps
import pandas as pd
import numpy as np
import json
import re
import bson
#import string

from machinelearn import machinetrain, recommendation, calculate_similarity, shopping_list

client = MongoClient("mongodb+srv://kimpeter:kimpeter@cluster0-lux2o.gcp.mongodb.net/machinetime?retryWrites=true")
db = client.machinetime

app = Flask(__name__)
    

@app.route("/get_recommendation", methods = ['POST'])
def get_recommendation():
  try:
    #data = json.loads(request.data)
    # data = request.form.get('order')
    data = request.form['order']
    order = data['order']
    reclist = []
    reclist = recommendation(order) # return an index list of recommended items   
    # Send POST request 
    #r = requests.post("http://example.com", data=reclist)  
    
    # insert into DB
    db.orderdata.insert_one(order)
    update_machine()
    
    resp = jsonify(order)
    resp.status_code = 200
    
    return resp
  except Exception, e:
    print "Failure"
    
    
def update_machine():
  print("updatetime")

  rows = []
  for doc in db.orderdata.find():
    cur =  doc['order'].encode("ascii").split(',')
    cur = list(map(int,cur))
    rows.append(cur)
  data = np.array(rows)    
  data = pd.DataFrame(data)
  print(data)
  # TRAIN DATA
  machinetrain(data)
    
@app.route('/hello', methods = ['GET'])
def hello():
    data = {
        'hello'  : 'world',
        'number' : 3
    }

    return jsonify(data)    
    
if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='0.0.0.0', port=port)
    