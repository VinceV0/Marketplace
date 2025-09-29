# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'Listing' class

# Any print statements are for testing purposes
import random

class Listing:
    # Array of known UNIQUE 6 digits numbers
    uniqueNums = []
    # Parameter datatypes are recommended but not enforced
    def __init__(self,  listingTitle:str, listingPrice:float, condition:str):
        # Calls a method to generate a unique randomly generated 6-digit number
        self.gen = self.genUnique()
        # Stores unique Object ID an integer
        self.__code = len(self.uniqueNums)
        # Stores the listing title
        self._listingTitle = listingTitle
        # Stores the listing price as a float
        self._listingPrice = listingPrice
        # Stores the condition of the listing - E.g. New, Used
        self._condition = condition
    
    # Generate a UNIQUE 6-digit integer
    def genUnique(self):
        # Generate a random 6-digit integer
        self.generate = random.randint(100000, 999999)
        # print(self.generate)
        if self.generate in self.uniqueNums:
            # If found to be a duplicate number, call itself again to generate another number
            # print("Duplicate value")
            self.genUnique()
        else:
            # If the generated number is unique it will append to the list of known unique numbers
            self.uniqueNums.append(self.generate)
            # print("Appended new unique number")
            # Returns the UNIQUE
            return self.generate

    # If in case the object is directly called it is easily identified by the code and title
    def __str__(self):
        return f"{self.__code}:{self.gen}:{self.GetListingTitle()}"
    
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
        self._fullinfo = f"{self.GetListingTitle()},${self.GetListingPrice()},{self.GetCondition()}"
        return self._fullinfo

def main():
    # # Test harness, putting in 2 objects, changing the first object

    # # First Object
    # listing1 = Listing("Apple", "2.00", "New")
    # # Printing the object code and the corresponding listing title
    # print(listing1)
    # # Print using method
    # print(f"{listing1.DisplayListing()}\n")

    # # Changing the first listing's properties
    # listing1.ListingTitle = "Pear"
    # listing1.ListingPrice = "3.99"
    # listing1.Condition = "Used"
    # # Reprinting the object code and the corresponding listing title - Should print same code but now different Listing Title
    # print(listing1)
    # # Print using method
    # print(f"{listing1.DisplayListing()}\n")
    
    # # Second object(listing)
    # listing2 = Listing("Banana", "2.50", "Used")
    # # Printing the object code and the corresponding listing title
    # print(listing2)
    # # Print using properties
    # print(f"{listing2.ListingTitle},${listing2.ListingPrice},{listing2.Condition}")
    pass

if __name__ == "__main__":
    main()
