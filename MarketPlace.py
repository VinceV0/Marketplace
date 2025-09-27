# Vince Vagay - 30036567
# Task 1
# This code is specifically derived from the UML Class Diagram
# This defines the 'MarketPlace' class which inherits from the 'Listing' class

from Listing import Listing

class MarketPlace(Listing):
    # Array of known UNIQUE 6 digits numbers
    uniqueNums = []
    # Parameter datatypes are recommended but not enforced
    def __init__(self, listingTitle:str, listingPrice:float, condition:str, description:str, phoneNum:str, email:str, sellerName:str, url:str):
        # Inheriting the parent class member variables
        super().__init__(listingTitle, listingPrice, condition)
        
        # Although the 6-digit integer generator method was inherited
        # 'code' was not inherited as it has a private access modifier, I have reinitilized it here
        # Stores Object ID
        self.__code = len(self.uniqueNums)
        self._description = description
        self._phoneNum = phoneNum
        self._email = email
        self._sellerName = sellerName
        self._url = url


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

    # Getter for SellerName
    def GetSellerName(self):
        return self._sellerName

    # Setter for SellerName
    def SetSellerName(self, sellerName):
        self._sellerName =  sellerName

    # Getter for URL
    def GetURL(self):
        return self._url

    # Setter for URL
    def SetURL(self, url):
        self._url = url

    # Properties
    Description = property(GetDescription, SetDescription)
    PhoneNum = property(GetPhoneNum, SetPhoneNum)
    Email = property(GetEmail, SetEmail)
    SellerName = property(GetSellerName,SetSellerName)
    Url = property(GetURL,SetURL)
    
    def MarketListingInfo(self):
        self._fullinfo = f"{self.GetCondition()}, {self.GetListingTitle()}, {self.GetListingPrice():.2f}, {self.GetDescription()}, {self.GetPhoneNum()}, {self.GetEmail()}, {self.GetSellerName()}, {self.GetURL()}"
        return self._fullinfo

def main():
    # Test Harness
                    # listingTitle:str, listingPrice:float, condition:str, description:str, phoneNum:str, email:str
    # First Listing
    listing1 = MarketPlace("Gold Watch", 244.99, "New", "This is a nice watch", "0215644434", "jeff34543@gmail.com", "Jeff Gold", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png")

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
    listing1.SellerName = "Jenny Gold"
    listing1.Url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2sSeQqjaUTuZ3gRgkKjidpaipF_l6s72lBw&s"

    # Printing the object code and the corresponding listing title
    print(f"\n{listing1}")
    # Print using method
    print(f"{listing1.MarketListingInfo()}\n")

    # Second listing
    listing2 = MarketPlace("Lamp", 25.00, "Used", "A nice tall lamp with a black lampshade", "0224554389", "greg458823@gmail.com", "Gregory Gordon", "https://pngimg.com/d/google_PNG19644.png")
    # Printing the object code and corresponding listing title
    print(listing2)
    # Print using properties in a more formatted manner
    print(f"Title:\t\t\t{listing2.ListingTitle} \nPrice:\t\t\t${listing2.ListingPrice:.2f} \nCondition:\t\t{listing2.Condition} \nDescription:\t\t{listing2.Description} \nPhone Number:\t\t{listing2.PhoneNum} \nEmail:\t\t\t{listing2.Email} \nSeller Name:\t\t{listing2.SellerName} \nURL:\t\t\t{listing2.Url}")
    # pass
if __name__ == "__main__":
    main()