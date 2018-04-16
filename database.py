
from flask_pymongo import MongoClient
mongo_ip = "172.17.0.8"
# mongo_ip = "localhost"
mongo_port = 27017
uri  = "mongodb://" + mongo_ip + ":" + str(mongo_port)+"/"
mongo = MongoClient(uri)

inventory=mongo['inventory']






