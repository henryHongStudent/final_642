from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self,paymentAmount, paymentDate , paymentID):
        self._paymentAmount = paymentAmount
        self._paymentDate = paymentDate
        self._paymentID = paymentID
        
    # getters and setters
    #------------------------------------------------------------#
    @property
    def paymentAmount(self):
        return self._paymentAmount
    
    @paymentAmount.setter
    @abstractmethod
    def paymentAmount(self, paymentAmount):
        self._paymentAmount = paymentAmount
    
    @property
    def paymentDate(self):
        return self._paymentDate
    
    @paymentDate.setter
    @abstractmethod
    def paymentDate(self, paymentDate):
        self._paymentDate = paymentDate
    
    @property
    def paymentID(self):
        return self._paymentID
    
    @paymentID.setter
    @abstractmethod
    def paymentID(self, paymentID):
        self._paymentID = paymentID
    #------------------------------------------------------------#
    
    # method
    #------------------------------------------------------------#
    @abstractmethod
    def process_payment(self):
        pass
    #------------------------------------------------------------#
    

class CreditCardPayment(Payment):
    def __init__(self, paymentAmount, paymentDate, paymentID, cardExpiryDate, cardNumber,cardType):
        super().__init__(paymentAmount, paymentDate, paymentID)
        self._cardExpiryDate = cardExpiryDate
        self._cardNumber = cardNumber
        self._cardType = cardType
    
    # getters and setters
    #------------------------------------------------------------#
    @property
    def cardType(self):
        return self._cardType
    @property
    def cardExpiryDate(self):
        return self._cardExpiryDate
    
    @cardExpiryDate.setter
    def cardExpiryDate(self, cardExpiryDate):
        self._cardExpiryDate = cardExpiryDate
    
    @property
    def cardNumber(self):
        return self._cardNumber
    
    @cardNumber.setter
    def cardNumber(self, cardNumber):
        self._cardNumber = cardNumber
    
    @property
    def paymentAmount(self):
        return self._paymentAmount  
    @paymentAmount.setter
    def paymentAmount(self, paymentAmount):
        if paymentAmount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        self._paymentAmount = paymentAmount
    
    @property
    def paymentDate(self):
        return self._paymentDate
    
    @paymentDate.setter
    def paymentDate(self, paymentDate):
        self._paymentDate = paymentDate 
    
    @property
    def paymentID(self):
        return self._paymentID
    
    @paymentID.setter
    def paymentID(self, paymentID):
        self._paymentID = paymentID
    
    #------------------------------------------------------------#
    
    # method
    #------------------------------------------------------------#
    def process_payment(self):
        print(f"Processing Credit Card Payment: Amount: {self.paymentAmount}, Date: {self.paymentDate}, ID: {self.paymentID}, Expiry Date: {self.cardExpiryDate}, Card Number: {self.cardNumber}, Card Type: {self.cardType}")
    #------------------------------------------------------------#
    

class DebitCardPayment(Payment):
    def __init__(self, paymentAmount, paymentDate, paymentID,bankName,debitCardNumber):
        super().__init__(paymentAmount, paymentDate, paymentID)
        self._bankName = bankName
        self._debitCardNumber = debitCardNumber
    
    # getters and setters
    #------------------------------------------------------------#
    @property
    def bankName(self):
        return self._bankName
    
    @bankName.setter
    def bankName(self, bankName):
        self._bankName = bankName
    
    @property
    def debitCardNumber(self):
        return self._debitCardNumber
    
    @debitCardNumber.setter
    def debitCardNumber(self, debitCardNumber):
        self._debitCardNumber = debitCardNumber
    
    @property
    def paymentAmount(self):
        return self._paymentAmount
    
    @paymentAmount.setter
    def paymentAmount(self, paymentAmount):
        if paymentAmount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        self._paymentAmount = paymentAmount
    
    @property
    def paymentDate(self):
        return self._paymentDate
    
    @paymentDate.setter
    def paymentDate(self, paymentDate):
        self._paymentDate = paymentDate
        
    @property
    def paymentID(self):
        return self._paymentID
    
    @paymentID.setter
    def paymentID(self, paymentID):
        self._paymentID = paymentID
        
    # method
    #------------------------------------------------------------#
    def process_payment(self):
        print(f"Processing Debit Card Payment: Amount: {self.paymentAmount}, Date: {self.paymentDate}, ID: {self.paymentID}, Bank Name: {self.bankName}, Debit Card Number: {self.debitCardNumber}")
    #------------------------------------------------------------#
    
    
