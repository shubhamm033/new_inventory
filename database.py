
from flask_pymongo import MongoClient,ASCENDING,DESCENDING
mongo_ip = "172.17.0.8"
# mongo_ip = "localhost"
mongo_port = 27017
uri  = "mongodb://" + mongo_ip + ":" + str(mongo_port)+"/"
mongo = MongoClient(uri)

inventory=mongo['binventory']



