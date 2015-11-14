from pymongo import MongoClient
from parser import *

# Insert ticker into database 
def insert_ticker(db, tick):
	report = scrapeSEC(tick)
	collection = db.SEC_collection
	posts = db.posts 
	posts.insert(report)
	return 

def print_tickers(db):
	posts = db.posts
	print posts.find_one()

if __name__ == '__main__':
	try:
	    mongo = MongoClient()
	    print "Connected successfully"
	except pymongo.errors.ConnectionFailure, e:
   		print "Could not connect to MongoDB: %s" % e 

   	db = mongo.sec.tickers

   	insert_ticker(db, "aapl")
   	insert_ticker(db, "goog")

	print_tickers(db)