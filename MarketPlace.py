# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'MarketPlace' class which inherits from the 'Listing' class

from Listing import Listing

class MarketPlace(Listing):
    # Array of known UNIQUE 6 digits numbers
    uniqueNums = []
    # Parameter datatypes are recommended but not enforced
    def __init__(self, listingTitle:str, listingPrice:float, condition:str, description:str, phoneNum:str, email:str):
        # Inheriting the parent class member variables
        super().__init__(listingTitle, listingPrice, condition)
        
        # Although the 6-digit integer generator method was inherited
        # 'code' was not inherited as it has a private access modifier, I have reinitilized it here
        # Stores Object ID
        self.__code = len(self.uniqueNums)
        self._description = description
        self._phoneNum = phoneNum
        self._email = email


    # If in case the object is directly called it is easily identified by the code and title
    def __str__(self):
        return f"{self.__code}:{self.gen}:{self.GetListingTitle()}"
    
    # Getter for Description
    def GetDescription(self):
        return self._description

    # Setter for Description
    def SetDescription(self, description):
        self._description = description
    
    # Getter for PhoneNum
    def GetPhoneNum(self):
        return self._phoneNum

    # Setter for PhoneNum
    def SetPhoneNum(self, phoneNum):
        self._phoneNum = phoneNum
    
    # Getter for Email
    def GetEmail(self):
        return self._email

    # Setter for Email
    def SetEmail(self, email):
        self._email = email

    # Properties
    Description = property(GetDescription, SetDescription)
    PhoneNum = property(GetPhoneNum, SetPhoneNum)
    Email = property(GetEmail, SetEmail)
    
    def MarketListingInfo(self):
        self._fullinfo = f"{self.GetCondition()}, {self.GetListingTitle()}, {self.GetListingPrice():.2f}, {self.GetDescription()}, {self.GetPhoneNum()}, {self.GetEmail()}"
        return self._fullinfo

def main():
    # Test Harness
                    # listingTitle:str, listingPrice:float, condition:str, description:str, phoneNum:str, email:str
    # First Listing
    listing1 = MarketPlace("Gold Watch", 244.99, "New", "This is a nice watch", "0215644434", "jeff34543@gmail.com")

    # Printing the object code and the corresponding listing title
    print(listing1)
    # Print using method
    print(listing1.MarketListingInfo())

    # Changing the first Listing's property
    listing1.ListingTitle = "Vintage Watch"
    listing1.ListingPrice = 123943.00
    listing1.Condition = "Used"
    listing1.Description = "This watch has been in the family for more than a century"
    listing1.PhoneNum = "0218743456"
    listing1.Email = "jenny3434@gmail.com"

    # Printing the object code and the corresponding listing title
    print(f"\n{listing1}")
    # Print using method
    print(f"{listing1.MarketListingInfo()}\n")

    # Second listing
    listing2 = MarketPlace("Lamp", 25.00, "Used", "A nice tall lamp with a black lampshade", "0224554389", "greg458823@gmail.com")
    # Printing the object code and corresponding listing title
    print(listing2)
    # Print using properties in a more formatted manner
    print(f"Title:\t\t\t{listing2.ListingTitle} \nPrice:\t\t\t${listing2.ListingPrice:.2f} \nCondition:\t\t{listing2.Condition} \nDescription:\t\t{listing2.Description} \nPhone Number:\t\t{listing2.PhoneNum} \nEmail:\t\t\t{listing2.Email}")
    pass

if __name__ == "__main__":
    main()