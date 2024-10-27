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
    
    
# def test_payment_processing():
#     # Test Credit Card Payment
#     try:
#         credit_payment = CreditCardPayment(
#             paymentAmount=100.00,
#             paymentDate='2024-10-19',
#             paymentID='CC123',
#             cardExpiryDate='12/25',
#             cardNumber='1234-5678-9012-3456',
#             cardType='Visa'
#         )
#         credit_payment.process_payment()  # Expected output showing details of the payment
#     except ValueError as e:
#         print(f"Credit Card Payment Error: {e}")

#     # Test Debit Card Payment
#     try:
#         debit_payment = DebitCardPayment(
#             paymentAmount=50.00,
#             paymentDate='2024-10-19',
#             paymentID='DC456',
#             bankName='Bank of New Zealand',
#             debitCardNumber='9876-5432-1098-7654'
#         )
#         debit_payment.process_payment()  # Expected output showing details of the payment
#     except ValueError as e:
#         print(f"Debit Card Payment Error: {e}")

#     # Test with invalid payment amount
#     try:
#         invalid_credit_payment = CreditCardPayment(
#             paymentAmount=-50.00,  # Invalid amount
#             paymentDate='2024-10-19',
#             paymentID='CC124',
#             cardExpiryDate='12/25',
#             cardNumber='1234-5678-9012-3456',
#             cardType='Visa'
#         )
#         invalid_credit_payment.process_payment()  # This should raise an error
#     except ValueError as e:
#         print(f"Invalid Credit Card Payment Error: {e}")

#     try:
#         invalid_debit_payment = DebitCardPayment(
#             paymentAmount=0,  # Invalid amount
#             paymentDate='2024-10-19',
#             paymentID='DC457',
#             bankName='Bank of New Zealand',
#             debitCardNumber='9876-5432-1098-7654'
#         )
#         invalid_debit_payment.process_payment()  # This should raise an error
#     except ValueError as e:
#         print(f"Invalid Debit Card Payment Error: {e}")

# test_payment_processing()

            