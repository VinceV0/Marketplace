# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'Property' class which inherits from the 'Listing' class

from Listing import Listing

# This Property class inherits from the Listing class
# This focuses on listings for Properties(Houses - Real estate)
# This class in addition to the Listing class, overrides the condition to say if the property is newly built or not
# It also adds where the property is located - the city, the suburb, and the number of bedrooms the listing has.
class Property(Listing):
    # Array of known UNIQUE 6 digits numbers
    uniqueNums = []
    # Parameter datatypes are recommended but not enforced
    # Condition has been overriden to a bool value, to say if the property is newly built or not
    def __init__(self, listingTitle:str, listingPrice:float, condition:bool, city:str, numBedrooms:int, suburb:str):
        # Inheriting the parent class member variables
        super().__init__(listingTitle, listingPrice, condition)
        
        # Although the 6-digit integer generator method was inherited
        # 'code' was not inherited as it has a private access modifier, I have reinitilized it here
        # Stores unique Object ID an integer
        self.__code = len(self.uniqueNums)
        # Stores the city the property is located in
        self._city = city
        # Stores the number of bedrooms the property has
        self._numBedrooms = numBedrooms
        # Stores the suburb the property is located in
        self._suburb = suburb

    # If in case the object is directly called it is easily identified by the code and title
    def __str__(self):
        return f"{self.__code}:{self.gen}:{self.GetListingTitle()}"
    
    # Getter for City
    def GetCity(self):
        return self._city

    # Setter for City
    def SetCity(self, city):
        self._city = city

    # Getter for NumBedrooms
    def GetNumBedrooms(self):
        return self._numBedrooms

    # Setter for NumBedrooms
    def SetNumBedrooms(self, numBedrooms):
        self._numBedrooms = numBedrooms

    # Getter for Suburb
    def GetSuburb(self):
        return self._suburb

    # Setter for Suburb
    def SetSuburb(self, suburb):
        self._suburb = suburb

    # # Getter for []
    # def Get[](self):
    #     return self._[]

    # # Setter for []
    # def Set[](self, []):
    #     self._[] = []

    # Properties
    City = property(GetCity, SetCity)
    NumBedrooms = property(GetNumBedrooms, SetNumBedrooms)
    Suburb = property(GetSuburb, SetSuburb)

    # Display Property listing information nicely
    def PropertyListingInfo(self):
        self._fullinfo = f"{self.GetListingTitle()}, {self.GetNumBedrooms()}, {self.GetCity()}, {self.GetListingPrice():.2f}, {self.GetSuburb()}, {self.GetCondition()}"
        return self._fullinfo

def main():
    # Test harness, 2 Properties, changing the first Property

    # First Property
    property1 = Property("67 Duncan Street", 656656.00, True, "Rotorua", 3, "Fenton Park")
    # Printing the object code and the corresponding property listing title
    print(property1)
    # Print using method
    print(property1.PropertyListingInfo())

    # Changing first Property's properties
    property1.ListingTitle = "5 Bell Road"
    property1.City = "Tauranga"
    property1.ListingPrice = 786784.00
    property1.NumBedrooms = 4
    property1.Suburb = "Papamoa"
    property1.Condition = False

    # Printing the object code and the corresponding property listing title
    print(f"\n{property1}")
    # Print using method
    print(f"{property1.PropertyListingInfo()}\n")

    # Second Property
    property2 = Property("4 Hatch Street", 853854.00, False, "Auckland", 2, "Albany")
    # Printing the object code and the corresponding property listing title
    print(property2)
    # Print using properties in a more formatted manner
    print(f"Street:\t\t\t{property2.ListingTitle} \nCity:\t\t\t{property2.City} \nSuburb:\t\t\t{property2.Suburb} \nPrice:\t\t\t${property2.ListingPrice:.2f} \nNumber of Bedrooms:\t{property2.NumBedrooms} \nNew build: \t\t{property2.Condition}")

if __name__ == "__main__":
    main()