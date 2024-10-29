from abc import ABC, abstractmethod

class Items(ABC):
    def __init__(self, itemName, itemPrice):
        self._itemName = itemName
        self._itemPrice = itemPrice
        self._sale_count = 0

    @abstractmethod
    def get_price(self):
        return self._itemPrice

    def get_name(self):
        return self._itemName

    def add_sale_count(self):
        self._sale_count += 1
    
    def get_sale_count(self):
        return self._sale_count
    def __str__(self):
        return f"{self._itemName}: ${self.get_price():.2f} (Sold: {self.get_sale_count()})"  

class Veggie(Items):
    def __init__(self, vegName):
        super().__init__(vegName, 0)  
        self._vegName = vegName

    @property
    def vegName(self):
        return self._vegName

    @vegName.setter
    def vegName(self, vegName):
        self._vegName = vegName
    
    def get_price(self):
        return self._itemPrice

    def __str__(self):
        return f"Vegetable: {self._vegName}"  


class WeightedVeggie(Veggie):
    def __init__(self, vegName, weight, weightPerKilo):
        super().__init__(vegName)
        self._weight = weight
        self._weightPerKilo = weightPerKilo
    
    def get_price(self):
        return self._weight * self._weightPerKilo

    def __str__(self):
        return f"Weighted Vegetable: {self._vegName}, Weight: {self._weight}kg, Price: ${self.get_price():.2f}"


class PackVeggie(Veggie):
    def __init__(self, vegName, numOfPack, pricePerPack):
        super().__init__(vegName)
        self._numOfPack = numOfPack
        self._pricePerPack = pricePerPack

    def get_price(self):
        return self._numOfPack * self._pricePerPack

    def __str__(self):
        return f"Packaged Vegetable: {self._vegName}, Packs: {self._numOfPack}, Price: ${self.get_price():.2f}"


class UnitPriceVeggie(Veggie):
    def __init__(self, vegName, pricePerUnit, quantity):
        super().__init__(vegName)
        self._pricePerUnit = pricePerUnit
        self._quantity = quantity

    def get_price(self):
        return self._pricePerUnit * self._quantity

    def __str__(self):
        return f"Unit Price Vegetable: {self._vegName}, Quantity: {self._quantity}, Price: ${self.get_price():.2f}"


class PremadeBox(Items):
    def __init__(self, boxSize, numOfBoxes):
        super().__init__("Premade Box", 0)
        self._boxSize = boxSize
        self._numOfBoxes = numOfBoxes
        self._boxContent = []
        
    def add_veggie(self, veggie: Veggie):
        self._boxContent.append(veggie)
    
    def get_price(self):
        total_price = sum(veggie.get_price() for veggie in self._boxContent) 
        self._itemPrice = total_price * self._numOfBoxes  
        return self._itemPrice 
    
    def get_veggie_names(self):
        return [veggie.get_name() for veggie in self._boxContent]

    def __str__(self):
        veggie_details = "\n".join(str(veggie) for veggie in self._boxContent)
        return f"Premade Box - Size: {self._boxSize}, Number of Boxes: {self._numOfBoxes}\nContents:{veggie_details}"

