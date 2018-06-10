
class product():
    conditionMap = ['new', 'slightly used', 'used', 'broken']

    def __init__(self, newOwnerID, newProductID, newProductDataID, newTitle, newDesc, newCondition, newCountry, newCity, newAuction, newPrice, newShippingType, newShippingPrice, newDateAdded, newDateExpires):
        self.ownerID = newOwnerID
        self.productID = newProductID
        self.productDataID = newProductDataID
        self.title = newTitle
        self.desc = newDesc
        self.condition = newCondition
        self.country = newCountry
        self.city = newCity
        self.auction = bool(newAuction)
        self.price = newPrice
        self.shippingType = newShippingType
        self.shippingPrice = newShippingPrice
        self.dateAdded = newDateAdded
        self.dateExpires = newDateExpires
