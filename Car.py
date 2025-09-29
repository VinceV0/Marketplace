# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'Car' class which inherits from the 'Listing' class

from Listing import Listing

class Car(Listing):
    # Array of known UNIQUE 6 digits numbers
    uniqueNums = []
    # Parameter datatypes are recommended but not enforced
    def __init__(self, listingTitle:str, listingPrice:float, condition:str, carRego:str):
        # Inheriting the parent class member variables
        super().__init__(listingTitle, listingPrice, condition)
        # Although the 6-digit integer generator method was inherited
        # 'code' was not inherited as it has a private access modifier, I have reinitilized it here
        # Stores unique Object ID an integer
        self.__code = len(self.uniqueNums)
        # Stores the registration number of the vehicle
        self._carRego = carRego

    # If in case the object is directly called it is easily identified by the code and title
    def __str__(self):
        return f"{self.__code}:{self.gen}:{self.GetListingTitle()}"
    
    # Getter for CarRego
    def GetCarRego(self):
        return self._carRego

    # Setter for CarRego
    def SetCarRego(self, carRego):
        self._carRego = carRego

    # Properties
    CarRego = property(GetCarRego, SetCarRego)

    # Display Car listing information nicely
    def CarListingInfo(self):
        self._fullinfo = f"{self.GetCondition()}, {self.GetListingTitle()}, {self.GetCarRego()}, {self.GetListingPrice():.2f}"
        return self._fullinfo

def main():
    # Test harness, 2 Cars, changing the first Car

    # First Car
    car1 = Car("2016 Ford Mustang", 79990.00, "New", "ROR432")

    # Printing the object code and the corresponding care listing title
    print(car1)
    # Print using method
    print(car1.CarListingInfo())

    # Changing the first Car's property
    car1.ListingTitle = "2018 Ford GT"
    car1.ListingPrice = 1950000.00
    car1.Condition = "Used"
    car1.CarRego = "324SDR"

    # Printing the object code and the corresponding car listing title
    print(f"\n{car1}")
    # Print using method
    print(f"{car1.CarListingInfo()}\n")

    # Second Car
    car2 = Car("2021 Rimac Nevera", 3752639.00, "New", "JDK349")
    # Printing the object code and corresponding car listing title
    print(car2)
    # Print using properties in a more formatted manner
    print(f"Car:\t\t\t{car2.ListingTitle} \nPrice:\t\t\t${car2.ListingPrice:.2f} \nCondition:\t\t{car2.Condition} \nRego:\t\t\t{car2.CarRego}")

if __name__ == "__main__":
    main()