# Vince Vagay - 30036567
# Task 3
# Processing CRUD Operations

# This sections was mostly hand done, with guidance from Google's Gemini 2.5 Flash

# Assuming MarketPlace.py and Mongo.py are in the same directory
from MarketPlace import MarketPlace
# We need the Mongo class itself to initialize the connection
from Mongo import Mongo 
from ChurFindsGUI import MarketplaceTester

# Performs the procesing of CRUD operations - Utilizing the code from Task 2 - Mongo.py
class CRUD:
    # Initialize
    def __init__(self, MongoDB):
        # The MongoDB is an instance of the Mongo class
        self.mongo = MongoDB

    # Creates a new MarketPlace/Listing object and appends it to the stored listings.
    # CODED USING GEMINI Utilizing my code from Task 2
    def AddListing(self, name, condition, price, seller_name, seller_phone, seller_email, desc, image_url=""):
        print(f"--- SUCCESS: AddListing CALLED ---")
        print(f"Name: {name}, Price: {price}, Desc: {desc}")
        try:
            # Create a new MarketPlace object using the clean data from the GUI
            new_listing = MarketPlace(
                listingTitle = name,
                listingPrice = price,
                condition = condition,
                description = desc,
                phoneNum = seller_phone,
                email = seller_email,
                sellerName = seller_name,
                url = image_url # Defaulted to empty string if not provided
            )

            # Append the new listing to the list obtained from Mongo
            self.mongo.get_StoredListings().append(new_listing)
            
            # Save the updated list back to the database
            self.mongo.saveToMongo()
            
            # The Listing class uses 'gen' for the unique 6-digit number
            print(f"SUCCESS: Added new listing '{name}' (Code: {new_listing.gen})")
            return True
        except Exception as e:
            print(f"ERROR: Failed to add listing: {e}")
            return False

    # Finds a listing by its index in the MongoDB - Stored Listings, updates its fields, and saves the changes.
    # UPDATE

    # HAND CODED BY VINCE VAGAY
    def EditListing(self, listing_code, name, condition, price, seller_name, seller_phone, seller_email, desc, index, image_url=""):
        # print(listing_code, name, condition, price, seller_name, seller_phone, seller_email, desc)
        print(f"Success index: {index}")
        self.mongo.get_StoredListings()[index].ListingTitle = name
        self.mongo.get_StoredListings()[index].ListingPrice = price
        self.mongo.get_StoredListings()[index].Condition = condition
        self.mongo.get_StoredListings()[index].Description = desc
        self.mongo.get_StoredListings()[index].SellerName = seller_name
        self.mongo.get_StoredListings()[index].PhoneNum = seller_phone
        self.mongo.get_StoredListings()[index].Email = seller_email
        self.mongo.get_StoredListings()[index].Url = image_url # This has not been implemented yet

        # Save the updated listings back to MongoDB
        self.mongo.saveToMongo()

    # HAND CODED BY VINCE VAGAY
    def DeleteListing(self, index):
        # Simulating the deletion of a listing
        # Delete the last listing and save to Mongo
        if len(self.mongo.get_StoredListings()) != 0:
            # Returns the title of what is being deleted
            print(f"DELETING: {self.mongo.get_StoredListings()[index].ListingTitle}")
            self.mongo.get_StoredListings().pop(index)
            # Save the updated listings back to MongoDB
            self.mongo.saveToMongo()
        else:
            print("Empty Database")