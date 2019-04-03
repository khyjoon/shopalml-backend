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
  # try:
  data = request.get_json()
  order = data['order']     # receive order field
  id = data['_id']          # receive id field
  
  reclist = recommendation(order) # return an index list of recommended items   
  
  # turn all items in order to 0
  for i in range(len(order)):
    order[i] = 0
  
  for var in reclist:
    order[var] = 1
  
  # Send POST request 
  # order[0] = 100
  # order[1] = 200
  # insert into DB
  orderstr = ','.join(map(str, order)) 
  db.orderdata.insert_one({'order': orderstr})
  update_machine()
  
  responseDict = { "order": order,        # create a dictionary. NOTE: python dict is a json Object
                    "_id" : id}
                    
  return jsonify(responseDict)
# except Exception, e:
  # return 'Failure'
  
    
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
        'number' : 3,
        'order' : 2
    }

    return jsonify(data)    
    
@app.route('/receive', methods = ['POST'])
def receive():
  data = request.get_json()
  order = data['order']
  id = data['_id']
  
  for i in range(len(order)):
    order[i] = 0
    
  newdict = { "order": order,
              "_id" : id}
  
  return jsonify(newdict)
    
if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='0.0.0.0', port=port)
    