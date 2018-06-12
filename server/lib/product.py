
class product():
    conditionMap = ['new', 'slightly used', 'used', 'broken']

    def __init__(self, newOwnerID, newProductID, newProductDataID, newTitle, newDesc, newImages, newCondition, newCountry, newCity, newAuction, newPrice, newShippingType, newShippingPrice, newDateAdded, newDateExpires):
        self.ownerID = newOwnerID
        self.productID = newProductID
        self.productDataID = newProductDataID
        self.title = newTitle
        self.desc = newDesc
        self.images = newImages
        self.condition = newCondition
        self.country = newCountry
        self.city = newCity
        self.auction = newAuction
        self.price = newPrice
        self.shippingType = newShippingType
        self.shippingPrice = newShippingPrice
        self.dateAdded = newDateAdded
        self.dateExpires = newDateExpires

    def asDict(self):
        result = dict()
        result = {'ownerID' : str(self.ownerID),
                'productID' : str(self.productID),
                'productDataID' : str(self.productDataID),
                'title' : str(self.title),
                'desc' : str(self.desc),
                'condition' : str(self.condition),
                'country' : str(self.country),
                'city' : str(self.city),
                'auction' : str(self.auction),
                'price' : str(self.price),
                'shippingType' : str(self.shippingType),
                'shippingPrice' : str(self.shippingPrice),
                'dateAdded' : str(self.dateAdded),
                'dateExpires' : str(self.dateExpires)}

        return result
