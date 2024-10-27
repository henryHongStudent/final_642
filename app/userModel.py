
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

box_veggie_association = Table(
    'box_veggie_association',
    Base.metadata,
    Column('box_id', Integer, ForeignKey('premade_box.id')),
    Column('veggie_id', Integer, ForeignKey('veggie.id'))
)

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    password = Column(String(100))
    type = Column(String(50),nullable=True)
    nextId = 1000

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

    # Define one-to-one relationship with Staff
    staff = relationship('Staff', back_populates='person', uselist=False)
    customer = relationship('Customer', back_populates='person', uselist=False)
    orders = relationship("Order", back_populates="person")
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        Person.nextId += 1
        self.id = Person.nextId

    def __str__(self):
        return f"Person({self.first_name} {self.last_name}, {self.username})"
    
    def get_login_user_details(self):
        """사용자의 모든 정보를 반환하는 메서드"""
        if self.type == 'staff':
            return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'type': self.type,
                'date_joined': self.staff.date_joined,
                'dept_name': self.staff.dept_name,
        
            }
        elif self.type == 'customer':
            return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'type': self.type,
                'cust_address': self.customer.cust_address,
                'cust_balance': self.customer.cust_balance,
                'max_owing': self.customer.max_owing
            }
    def get_all_user(self):
            """사용자의 모든 정보를 반환하는 메서드"""
            return {
                    'id': self.id,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'username': self.username,
                    'type': self.type,
                    'cust_address': self.customer.cust_address,
                    'cust_balance': self.customer.cust_balance,
                    'max_owing': self.customer.max_owing
                }



class Staff(Person):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    date_joined = Column(Date)
    dept_name = Column(String(50))
    
    # Define back reference to Person
    person = relationship('Person', back_populates='staff', uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }
    def __init__(self, first_name, last_name, username, password, date_joined, dept_name):
        super().__init__(first_name, last_name, username, password)  # Call parent constructor
        self.date_joined = date_joined
        self.dept_name = dept_name

    def __str__(self):
        return f"Staff({self.person.first_name} {self.person.last_name}, {self.person.username})"
    
    
class Customer(Person):
    __tablename__ = 'customers'
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    cust_address = Column(String(100))
    cust_balance = Column(Float)
    max_owing = Column(Float)
    list_of_orders = relationship("Order", back_populates="customer")
    list_of_payments = relationship("Payment", back_populates="customer")
    __mapper_args__ = { 
        'polymorphic_identity': 'customer'
    }
    person = relationship('Person', back_populates='customer', uselist=False)

    def __init__(self, first_name, last_name, username, password, cust_address, cust_balance, max_owing):
        super().__init__(first_name, last_name, username, password)  # Call parent constructor
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = max_owing

    def __str__(self):
        return f"Customer({self.person.first_name} {self.person.last_name}, {self.person.username})"


    def process_payment(self, amount, payment_method):
        if payment_method == 'credit_card':
            # Implement credit card payment logic
            pass
        elif payment_method == 'debit_card':
            # Implement debit card payment logic
            pass
        elif payment_method == 'account_charge':
            if self.cust_balance >= amount:
                self.cust_balance -= amount
                return True
            else:
                return False
        return False

    
    
class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customers'
    id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    discount_rate = Column(Float)
    max_credit = Column(Float)
    min_balance = Column(Float)
    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    def __init__(self, first_name, last_name, username, password, cust_address, cust_balance, max_owing, 
                 discount_rate, max_credit, min_balance):
        # Call the parent class (Customer) constructor
        super().__init__(first_name, last_name, username, password, cust_address, cust_balance, max_owing)
        self.discount_rate = discount_rate
        self.max_credit = max_credit
        self.min_balance = min_balance

    def __str__(self):
        return f"CorporateCustomer({self.first_name} {self.last_name}, {self.username}, Address: {self.cust_address}, Discount: {self.discount_rate})"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_person_id = Column(Integer, ForeignKey('persons.id'))
    order_date = Column(Date)
    order_number = Column(String(30), unique=True)
    order_status = Column(String(30))
    
    person = relationship("Person", back_populates="orders")
    customer = relationship("Customer", back_populates="list_of_orders")
    order_lines = relationship("OrderLine", back_populates="order")  # 추가된 관계

    def __init__(self, order_customer, order_date, order_number, order_status):
        self.order_person_id = order_customer
        self.order_date = order_date
        self.order_number = order_number
        self.order_status = order_status

    def __str__(self):
        return f"Order({self.order_number}) - {self.order_status} - {self.order_date} - {self.order_person_id})"


class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    order = relationship("Order", back_populates="order_lines")
    item = relationship("Item", back_populates="order_lines")
    quantity = Column(Integer)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    vegName = Column(String(50))
    type = Column(String(50))
    
    order_lines = relationship("OrderLine", back_populates="item")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'item'
    }
    

    
    

class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    vegName = Column(String(50))
    weighted_veggie = relationship("WeightedVeggie", uselist=False, back_populates="veggie")
    pack_veggie = relationship("PackVeggie", uselist=False, back_populates="veggie")
    unit_price_veggie = relationship("UnitPriceVeggie", uselist=False, back_populates="veggie")
    __mapper_args__ = {
        'polymorphic_identity': 'veggie'
    }

    def get_price(self):
        if self.weighted_veggie:
            return self.weighted_veggie.weight * self.weighted_veggie.weightPerKilo
        elif self.pack_veggie:
            return self.pack_veggie.numOfPack * self.pack_veggie.pricePerPack
        elif self.unit_price_veggie:
            return self.unit_price_veggie.pricePerUnit * self.unit_price_veggie.quantity
        else:  # None of the above conditions are met
            return 0  # 또는 적절한 기본값


class WeightedVeggie(Base):
    __tablename__ = 'weighted_veggie'
    id = Column(Integer, primary_key=True)
    veggie_id = Column(Integer, ForeignKey('veggie.id'))
    weight = Column(Float)
    weightPerKilo = Column(Float)
    veggie = relationship("Veggie", back_populates="weighted_veggie")

class PackVeggie(Base):
    __tablename__ = 'pack_veggie'
    id = Column(Integer, primary_key=True)
    veggie_id = Column(Integer, ForeignKey('veggie.id'))
    numOfPack = Column(Integer)
    pricePerPack = Column(Float)
    veggie = relationship("Veggie", back_populates="pack_veggie")

class UnitPriceVeggie(Base):
    __tablename__ = 'unit_price_veggie'
    id = Column(Integer, primary_key=True)
    veggie_id = Column(Integer, ForeignKey('veggie.id'))
    quantity = Column(Integer)
    pricePerUnit = Column(Float)
    veggie = relationship("Veggie", back_populates="unit_price_veggie")
    
    

class PremadeBox(Item):
    __tablename__ = 'premade_box'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    vegName = Column(String(50))
    boxSize = Column(String(50))
    numOfBoxes = Column(Integer)
    price = Column(Float)
    boxContent = relationship('Veggie', 
                              secondary=box_veggie_association,
                              backref='boxes')

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box'
    }
    
    def get_total_price(self):
        return sum(veggie.get_price() for veggie in self.boxContent)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    payment_id = Column(String(50), unique=True)
    payment_date = Column(Date)
    payment_amount = Column(Float)
    payment_method = Column(String(50))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="list_of_payments")
    nextId = 2114
    def __init__(self, payment_id, payment_date, payment_amount, payment_method, customer_id):
        self.payment_id = f"PAY{Payment.nextId}"  # nextId 사용
        Payment.nextId += 1  # 다음 번호를 위해 증가
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.payment_method = payment_method
        self.customer_id = customer_id
    
    
class CreditCardPayment(Payment):
        __tablename__ = 'credit_card_payments'
        id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
        card_expiry_date = Column(Date)
        card_number = Column(String(16))
        card_type = Column(String(20))

        def __init__(self, payment_id, payment_date, payment_amount, payment_method, customer_id, card_expiry_date, card_number, card_type):
            super().__init__(payment_id, payment_date, payment_amount, payment_method, customer_id)
            self.card_expiry_date = card_expiry_date
            self.card_number = card_number
            self.card_type = card_type

class DebitCardPayment(Payment):
    __tablename__ = 'debit_card_payments'
    id = Column(Integer, ForeignKey('payments.id'), primary_key=True)
    bank_name = Column(String(50))
    debit_card_number = Column(String(16))
    
    def __init__(self, payment_id, payment_date, payment_amount, payment_method, customer_id, bank_name, debit_card_number):
        super().__init__(payment_id, payment_date, payment_amount, payment_method, customer_id)
        self.bank_name = bank_name
        self.debit_card_number = debit_card_number
    



