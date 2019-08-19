#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import bottle
from bottle import route, run, request, abort
import datetime

#Database connections
connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

#CRUD Functions
#Create
def insert_document(document):
    try:
        result=collection.insert_one(document)
    except ValidationError as ve:
        abort(400, str(ve))
    if result:
      print "true"
    else:
      print "false"
    return result
  
#Read
def get_document(document):
    print(document)
    result=collection.find_one(document)
    if not result:
        abort(400, "document not found")
    return result

#Update
def update_document(key, value, document):
    result=collection.update({key:value},{'$set': document}, upsert=False,multi=False)
    if not result:
        abort(400, "document not updated")
    return result

#Delete
def delete_document(document):
    result=collection.delete_one(document)
    if not result:
        abort(400, "document not found")
    return result


  
#RESTful Functions
#POST
@route('/createStock', method='POST')
def put_document():
  data = request.body.readline() 
  entity = json.loads(data)
  
  if not data:
    abort(400, 'No data received')
    
  if not entity.has_key('Ticker'):
    abort(400, 'No Ticker specified') 
    
  result = insert_document(entity) 
  return json.loads(json.dumps(entity, indent=4, default=json_util.default))
  
#READ
@route('/getStock', method='GET')
def read_doc():
  data = {'Ticker': request.query.Ticker}
  entity = get_document(data) 

  return json.loads(json.dumps(entity, indent=4, default=json_util.default))

#UPDATE
@route('/updateStock', method='GET')
def update_doc():
  ticker = request.query.Ticker
  result = {"result": request.query.result}
  entity = update_document("Ticker", ticker, result) 
       
  if not entity:
    abort(404, "No document found to update")
  
  return json.loads(json.dumps(entity, indent=4, default=json_util.default))
  return entity.deleted_count

#DELETE
@route('/deleteStock', method='GET')
def delete_doc():

  result = {"Ticker": request.query.Ticker}
  entity = delete_document(result)
  
  if not entity:
    abort(404, "Document could not be deleted")

  return result

if __name__ == '__main__':
 #app.run(debug=True)
 run(host='localhost', port=8080)