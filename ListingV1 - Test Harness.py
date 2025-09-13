# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'Listing' class

import random

class Listing:
    # Parameter datatypes are recommended but not enforced
    def __init__(self,  listingTitle:str, listingPrice:float, condition:str):
        # Generate a random 6-digit integer
        self.gen = random.randint(100000, 999999)
        # Stores Object ID
        self.__code = self.gen
        self._fullinfo = f"User is selling a {self.GetCondition} {self.GetListingTitle} for {self.GetListingPrice}"
        self._listingTitle = listingTitle
        self._listingPrice = listingPrice
        self._condition = condition
    
    # If in case the object is directly called it is easily identified by the code and title
    def __str__(self):
        return f"{self.__code}:{self.GetListingTitle}"
    
    # Getter for Listing Title
    def GetListingTitle(self):
        return self._listingTitle

    # Setter for Listing Title
    def SetListingTitle(self, listingTitle):
        self._listingTitle = listingTitle

    # Getter for Listing Price
    def GetListingPrice(self):
        return self._listingPrice

    # Setter for Listing Price
    def SetListingPrice(self, listingPrice):
        self._listingPrice = listingPrice

    # Getter for Condition
    def GetCondition(self):
        return self._condition

    # Setter for Condition
    def SetCondition(self, condition):
        self._condition = condition

    # Properties
    ListingTitle = property(GetListingTitle, SetListingTitle)
    ListingPrice = property(GetListingPrice, SetListingPrice)
    Condition = property(GetCondition, SetCondition)

    # Displays the information nicely
    def DisplayListing(self):
        return f"{self.GetListingTitle()}, {self.GetListingPrice()}, {self.GetCondition()}"

def main():
    # Test harness, putting in 2 objects, changing the first object
    listing1 = Listing("Apple", "2", "New")
    listing2 = Listing("Banana", "2", "Used")
    listing1.ListingTitle = "Pear"
    listing1.ListingPrice = "3"
    listing1.Condition = "Used"
    # Display using method and printing properties
    print(listing1.DisplayListing())
    print(f"{listing2.ListingTitle}, {listing2.ListingPrice}, {listing2.Condition}")

if __name__ == "__main__":
    main()
