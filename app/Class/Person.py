
from abc import ABC, abstractmethod


class Person(ABC):#-
    def __init__(self,firstName,lastName,password,username):
    #properties
    #------------------------------------------------------------#
        self._firstName = firstName
        self._lastName = lastName
        self._password = password
        self._username = username
    #------------------------------------------------------------#
        
    # getters and setters 
    #------------------------------------------------------------#
    @property
    def firstName(self):
            return self._firstName
        
    @firstName.setter
    @abstractmethod
    def firstName(self, firstName):
           pass
            
    @property
    def lastName(self):
            return self._lastName
        
    @lastName.setter
    @abstractmethod
    def lastName(self, lastName):
        pass
        
    @property
    def username(self):
        return self._username
    #------------------------------------------------------------#

    # Login & Logout method
    @abstractmethod
    def login(self):
        pass
        
    @abstractmethod
    def logout(self):
        pass
    #------------------------------------------------------------#
class Staff(Person):
    def __init__(self,firstName,lastName,password,username,dateJoined,deptName,listOfCustomers,listOfOrders,premadeBoxes,staffID,veggies):
        super().__init__(firstName,lastName,password,username)
        self._dateJoined = dateJoined
        self._deptName = deptName
        self._listofCustomers = []
        self._listOfOrders = []
        self._premadeBoxes = []
        self._staffID = staffID
        self._veggies = []
    
    # getters and setters
    #------------------------------------------------------------#
    @Person.firstName.setter
    def firstName(self, firstName):
        self._firstName = firstName
    
    @Person.lastName.setter
    def lastName(self, lastName):
        self._lastName = lastName
    #------------------------------------------------------------#
        
    # method 
    #------------------------------------------------------------#
    def login(self):
        print(f"{self._username} logged in.")
    
    def logout(self):
        print(f"{self._username} logged out.")
        
    def get_all_customers(self):
        return self._listofCustomers

    
    def add_customer(self, customer):
        self._listofCustomers.append(customer)
    
    def get_all_orders(self):
        return self._listOfOrders
    
    def add_order(self, order):
        self._listOfOrders.append(order)
    
    def get_premadeBoxes(self):
        return self._premadeBoxes
    
    def add_premadeBox(self, premadeBox):
        self._premadeBoxes.append(premadeBox)
    
    def get_veggies(self):
        return self._veggies
    
    def add_veggie(self, veggie):
        self._veggies.append(veggie)
    #------------------------------------------------------------#
    
class Customer(Person):
    def __init__(self,firstName,lastName,password,username,custAddress,custBalance,custID,maxOwing):
        super().__init__(firstName,lastName,password,username)
        self._custAddress = custAddress
        self._custBalance = custBalance
        self._custID = custID
        self._maxOwing = maxOwing
        
    #getters and setters
    #------------------------------------------------------------#
    @Person.firstName.setter
    def firstName(self, firstName):
        self._firstName = firstName
        
    @Person.lastName.setter
    def lastName(self, lastName):
        self._lastName = lastName
            
    #------------------------------------------------------------#
        
    # methods
    #------------------------------------------------------------#
    def deposit(self, amount):
            self._custBalance += amount
        
    #method
    #------------------------------------------------------------#
    def login(self):
        print(f"{self._username} logged in.")
    
    def logout(self):
        print(f"{self._username} logged out.")
    #------------------------------------------------------------#   

class CorporateCustomer(Customer):
    def __init__(self, firstName, lastName, password, username, custAddress, custBalance, custID, maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName, lastName, password, username, custAddress, custBalance, custID, maxOwing)
        self._discountRate = discountRate
        self._maxCredit = maxCredit
        self._minBalance = minBalance
        
    # getter and setters
    #------------------------------------------------------------#
    @property
    def discountRate(self):
        return self._discountRate
        
    @discountRate.setter
    def discountRate(self, discountRate):
        self._discountRate = discountRate
    
    @property
    def maxCredit(self):
        return self._maxCredit
        
    @maxCredit.setter
    def maxCredit(self, maxCredit):
        self._maxCredit = maxCredit
    
    @property
    def minBalance(self):
        return self._minBalance
        
    @minBalance.setter
    def minBalance(self, minBalance):
        self._minBalance = minBalance

def main():
    # Staff 인스턴스 생성
    staff_member = Staff("Alice", "Johnson", "securePassword", "ajohnson", "2023-01-01", "Sales", [], [], [], "S001", [])
    
    # Staff 메소드 테스트
    print("Staff Info:")
    print(f"Name: {staff_member.firstName} {staff_member.lastName}")
    staff_member.login()  # Staff 로그인
    staff_member.logout()  # Staff 로그아웃

    # Customer 인스턴스 생성
    customer1 = Customer("Bob", "Smith", "password", "bsmith", "123 Street", 100.0, "C001", 50.0)
    
    # Customer 메소드 테스트
    print("\nCustomer Info:")
    print(f"Name: {customer1.firstName} {customer1.lastName}")
    customer1.deposit(50.0)  # 잔고에 50 추가
    print(f"New Balance: {customer1._custBalance}")  # 업데이트된 잔고 출력
    customer1.login()  # Customer 로그인
    customer1.logout()  # Customer 로그아웃

    # CorporateCustomer 인스턴스 생성
    corp_customer = CorporateCustomer("Charlie", "Brown", "corpPassword", "cbrown", "456 Avenue", 500.0, "C002", 100.0, 0.1, 1000.0, 200.0)
    
    # CorporateCustomer 메소드 테스트
    print("\nCorporate Customer Info:")
    print(f"Name: {corp_customer.firstName} {corp_customer.lastName}")
    print(f"Discount Rate: {corp_customer.discountRate}")
    print(f"Max Credit: {corp_customer.maxCredit}")
    print(f"Min Balance: {corp_customer.minBalance}")
    corp_customer.login()  # CorporateCustomer 로그인
    corp_customer.logout()  # CorporateCustomer 로그아웃
if __name__ == "__main__":
    main()