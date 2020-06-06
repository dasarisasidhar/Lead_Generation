from pymongo import MongoClient
import os
import googlemaps 

class dev_config():
    #object
    DEBUG = False
    TESTING = False
    admin_id = "sasidharraju.d@gmail.com"
    password = "supply@telyport"
    DATABASE_URI =  MongoClient('localhost', 27017) #mongo_db uses local host to store data 
    #smtp_id="dasarisasidhar.d@gmail.com"
    #smtp_password="joxqynnzjnisovxe"
    secret_key = os.urandom(24)
    jwt_key = "test_key"
    maps_key = googlemaps.Client(key = "AIzaSyCFUBzYLW1sVSF2Q8laM_Sbo9JhOKqYiU0")

class ProductionConfig():
    DATABASE_URI = ''

class DevelopmentConfig():
    DEBUG = True
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''
