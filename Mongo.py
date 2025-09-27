# Vince Vagay - 30036567
# Task 2
# MongoDB Incorporation

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

from MarketPlace import MarketPlace
from pprint import pprint

uri =

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

storedListings = []

try:
    client.admin.command('ping')
    # print("Pinged your deployment. You successfully connected to MongoDB!")
    mydb = client["Marketplace"]            # Pointing to the 'Marketplace' database
    mycollection = mydb["market"]           # Pointing to the 'market' collection

    listings = mycollection.find({})
    
    for listing in listings:
        print(f"Listing title: '{listing['ListingTitle']}'")
        listing = MarketPlace(listing['ListingTitle'], listing['ListingPrice'], listing['Condition'], listing['Description'], listing['PhoneNum'], listing['Email'], listing['sellerName'], listing['url'])
        storedListings.append(listing)
        
    for x in storedListings:
        print(x.MarketListingInfo())
except Exception as e:
    print(e)