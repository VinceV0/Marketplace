# Vince Vagay - 30036567
# Task 2
# MongoDB Incorporation

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

from MarketPlace import MarketPlace

class Mongo:
    def __init__(self):
        self.uri =

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

        # Stores the objects(listings) from the MongoDB
        self.storedListings = []

        try:
            # self.client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
            self.mydb = self.client["Marketplace"]            # Pointing to the 'Marketplace' database
            self.mycollection = self.mydb["market"]           # Pointing to the 'market' collection

            listings = self.mycollection.find({})

            for listing in listings:
                # print(f"Listing title: '{listing['ListingTitle']}'")
                listing_obj = MarketPlace(listing['ListingTitle'], listing['ListingPrice'], listing['Condition'], listing['Description'], listing['PhoneNum'], listing['Email'], listing['SellerName'], listing['Url'])
                self.storedListings.append(listing_obj)

            # for x in self.storedListings:
            #     print(x.MarketListingInfo())
        except Exception as e:
            print(e)

    # Getter for displaying the stored listings
    def get_StoredListings(self):
        return self.storedListings
    
    def saveToMongo(self):
        try:
            # Clear the collection to handle updates
            self.mycollection.delete_many({})
            # Prepare documents
            documents = []
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
                documents.append(details)
            # Insert/append all documents
            if documents:
                self.mycollection.insert_many(documents)
            print("Successfully saved listings to MongoDB")
        except Exception as e:
            print(f"Error in saving to Mongo: {e}")

def main():
    # Test harness, pulling from MongoDB and changing a listing, creating a listing
    mongo = Mongo()
####################################################################################################################
    # UPDATE
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
    # listing1 = MarketPlace("Lamp", 25.00, "Used", "A nice tall lamp with a black lampshade", "0224554389", "greg458823@gmail.com", "Gregory Gordon", "https://pngimg.com/d/google_PNG19644.png")
    # # Append the new listing to the stored listings
    # mongo.get_StoredListings().append(listing1)

    # # Save the updated listings back to MongoDB
    # mongo.saveToMongo()
####################################################################################################################
    # DELETE
    # Simulating the deletion of a listing
    # Delete the last listing and save to Mongo
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
            print(f"index: {i}, code: {i + 1}")
        i += 1
    # From this I can delete the listing based on the index
    
if __name__ == "__main__":
    main()
