
class Order:
    def __init__(self,orderCustomer,orderDate,orderNumber,orderStatus):
        self._orderCustomer = orderCustomer
        self._orderDate = orderDate
        self._orderNumber = orderNumber
        self._orderStatus = orderStatus
        self._listOfItems  = []
        
    
    # getters and setters
    #------------------------------------------------------------#
    @property
    def orderCustomer(self):
        return self._orderCustomer
    
    @orderCustomer.setter
    def orderCustomer(self, value):
        self._orderCustomer = value
    
    @property
    def orderDate(self):
        return self._orderDate
    
    @orderDate.setter
    def orderDate(self, value):
        self._orderDate = value
    
    @property
    def orderNumber(self):
        return self._orderNumber
    
    @orderNumber.setter
    def orderNumber(self, value):
        self._orderNumber = value
    
    @property
    def orderStatus(self):
        return self._orderStatus
    
    @orderStatus.setter
    def orderStatus(self, value):
        self._orderStatus = value
    #------------------------------------------------------------#
    # method
    #------------------------------------------------------------#
    def add_listOfItems (self, orderItem):
        self._listOfItems .append(orderItem)
    #------------------------------------------------------------#
    
class OrderLine(Order):
    def __init__(self,itemNumber):
        self._itemNumber = itemNumber
        self._anItem = None
        
    # getters and setters
    #------------------------------------------------------------#
    @property
    def itemNumber(self):
        return self._itemNumber
    
    @itemNumber.setter
    def itemNumber(self, value):
        self._itemNumber = value
        
    @property
    def anItem(self):
        return self._anItem
    
    @anItem.setter
    def anItem(self, value):
        self._anItem = value
    #------------------------------------------------------------#
    # method
    #------------------------------------------------------------#
    
    
    
