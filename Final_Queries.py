#!/usr/bin/python
import json
from bson import json_util
from pymongo import MongoClient
import bottle
from bottle import route, run, request, abort
from datetime import datetime
import pprint


connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

#Part 3. A. i
#function to find the number of documents in the low to high ranges of quick ratio values
def find_quickratio(low, high):
  query = {'50-Day Simple Moving Average':{'$lt': high, '$gt': low}}
  result = collection.find(query).count()
  return result

def main():
  
  print(find_quickratio(1, 5))
  
main()

 
#NEW FUNCTION THAT I CREATED FOR ENHANCEMENT
#Part 3. A. ii.  
#function created to take in input as a string and return documents with that matching key
def findSimilarIndustries(industry, dbName=defaultDBName, collectionName=defaultCollectionName):
  collection = connect_to_collection(dbName, collectionName)
  try:
    result = collection.find({"Industry": industry}, {"Ticker":1, "_id": False})
  except pymongo.errors.PyMongoError as ve:
  return (ve)
  return result

def main():
  
  print(findSimilarIndustries("Asset Management"))

main()

#Part 3. B. Aggregation Pipeline
#helps to find and sort various companies depending on what the user inputs
def findOutstandingCompaniesBySector(sector):
  result = collection.aggregate([
          {"$match": {"Sector": sector}},
          {"$group": {
              "_id": "$Industry",
              "Shares Outstanding": {"$sum":  "$Shares Outstanding"}
          }}
      ])
  return result
  
def main():
  
  print(findOutstandingCompaniesBySector("Healthcare"))
  
main()


#Advanced Queries
#Part 4. C. i.
@route('/stocks/api/v1.0/stockReport', method='POST')
def getReport():
read_result = []
for tickerSymbol in request.json.list:
read_result.append(read_document({"Ticker": tickerSymbol}))
print(read_result)
if(isinstance(read_result, Exception)):
print('exeption')
abort(500, "Database Error")
return json.dumps(read_result, sort_keys=True, indent=4, default=json_util.default)


#Part 4. C. ii.
@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
def portfolio(industry = None): 
try: 
findOutstandingCompaniesbySector = [{"$match":{"Industry":industry}},{"$project":{
"Company":1,"Price":1}},{"$sort":{"Price":-1}},{"$limit":5}]

stockResults = list(db.stocks.aggregate(findOutstandingCompaniesbySector))
return json.dumps(stockResults, indent=4, default=json_util.default) 

except NameError:
abort(404, 'No parameter for id %s' % id)



