# Vince Vagay - 30036567
# Task 2
# MongoDB Incorporation

# Using Pymongo to read and write from the MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

# Using the MarketPlace class
from MarketPlace import MarketPlace

# This Mongo class is used for pushing and pulling data from the Mongo Database and utilizes pymongo to do this
# I can read from the database, put the data into the MarketPlace class to create objects
# I can also then write to the database with any changes made to the imported data
# While the data is in the Python program I can perform Create, Read, Update and Delete operations on it
# I can also get the index of a specific listing
class Mongo:
    # Constructor initializes the connection to the MongoDB
    # Reads from the MongoDB collection and imports objects(listings) into a 'listings' list
    def __init__(self):
        # Connection to MongoDB cluster
        self.uri = "mongodb+srv://30036567:1035@cluster0.9m2co.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

        # Stores the objects(listings) from the MongoDB
        self.storedListings = []

        try:
            # self.client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
            self.mydb = self.client["Marketplace"]            # Pointing to the 'Marketplace' database
            self.mycollection = self.mydb["market"]           # Pointing to the 'market' collection
            
            # Gets/reads/finds all the listings
            listings = self.mycollection.find({})
            
            # Every listing in the collection passes it's values into the MarketPlace parameters
            # Each listing is an object
            for listing in listings:
                # print(f"Listing title: '{listing['ListingTitle']}'")
                listing_obj = MarketPlace(listing['ListingTitle'], listing['ListingPrice'], listing['Condition'], listing['Description'], listing['PhoneNum'], listing['Email'], listing['SellerName'], listing['Url'])
                # Each listing is appended into a list of objects
                self.storedListings.append(listing_obj)

            # for x in self.storedListings:
            #     print(x.MarketListingInfo())
        # If in case of an error, it's displayed
        except Exception as e:
            print(e)

    # Getter for displaying the stored listings
    def get_StoredListings(self):
        return self.storedListings
    
    # Method that saves the list of 'listings' objects into the MongoDB
    def saveToMongo(self):
        try:
            # Clear the collection to handle updates
            self.mycollection.delete_many({})
            # Prepare documents
            documents = []
            # Every listing passes its property getter value to the corresponding key
            for listing in self.storedListings:
                details = {
                    'gen': listing.gen,
                    'ListingTitle': listing.ListingTitle,
                    'ListingPrice': listing.ListingPrice,
                    'Condition': listing.Condition,
                    'Description': listing.Description,
                    'PhoneNum': listing.PhoneNum,
                    'Email': listing.Email,
                    'SellerName': listing.SellerName,
                    'Url': listing.Url
                }
                # Append the listing to the list of documents
                documents.append(details)
            # Insert/append all documents to MongoDB using insert_many
            # If there are documents
            if documents:
                self.mycollection.insert_many(documents)
            # On success it prints this statement
            print("Successfully saved listings to MongoDB")
        # On failure it prints the error returned
        except Exception as e:
            print(f"Error in saving to Mongo: {e}")

def main():
    # Test harness, pulling from MongoDB and changing a listing, creating a listing
    mongo = Mongo()
####################################################################################################################
    # # UPDATE
    # # Reading the first listing and it's price
    # print(f"{mongo.get_StoredListings()[0].ListingTitle} ${mongo.get_StoredListings()[0].ListingPrice}")

    # # Changing the listing price of that item
    # mongo.get_StoredListings()[0].ListingPrice = 5.01
    # # Reprinting it's information
    # print(f"{mongo.get_StoredListings()[0].ListingTitle} ${mongo.get_StoredListings()[0].ListingPrice}")

    # # Save the updated listings back to MongoDB
    # mongo.saveToMongo()
####################################################################################################################
    # # CREATE
    # # Simluation creating a new listing
    # listing1 = MarketPlace("Watch", 25, "Used", "A nice tall lamp with a black lampshade", "0224554389", "greg458823@gmail.com", "Gregory Gordon", "https://pngimg.com/d/google_PNG19644.png")
    # # Append the new listing to the stored listings
    # mongo.get_StoredListings().append(listing1)

    # # Save the updated listings back to MongoDB
    # mongo.saveToMongo()
####################################################################################################################
    # # DELETE
    # # Simulating the deletion of a listing
    # # Delete the last listing and save to Mongo
    # if len(mongo.get_StoredListings()) != 0:
    #     mongo.get_StoredListings().pop(len(mongo.get_StoredListings())- 1)
    #     # Save the updated listings back to MongoDB
    #     mongo.saveToMongo()
    # else:
    #     print("Empty Database")
####################################################################################################################
    # GET INDEX
    # Code to cycle through listing titles until it finds 'Lamp'
    # Prints the index in the list as well as the expected 'code'
    i = 1
    while i < len(mongo.get_StoredListings()):
        if mongo.get_StoredListings()[i].ListingTitle == "Lamp":
            print(f"index: {i}")
        i += 1
    # From this I can delete/edit the listing based on the index

if __name__ == "__main__":
    main()
