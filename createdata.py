from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,join,with_polymorphic
from decimal import Decimal

from app.userModel import Base,UnitPriceVeggie, CreditCardPayment, DebitCardPayment, PremadeBox, Person, Staff, Customer, CorporateCustomer, Order, OrderLine, Item, Veggie, WeightedVeggie, PackVeggie

# 엔진 생성
engine = create_engine('mysql+pymysql://root:Tmd%4078799858@localhost:3306/final_642', echo=True)
Base.metadata.drop_all(engine)
# # 데이터베이스 테이블 생성
Base.metadata.create_all(engine)


def create_mock_data():
    # Create engine and session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 2. Create Staff records (2)
        staff1 = Staff(
            first_name="Michael",
            last_name="Johnson",
            username="mjohnson",
            password="staff123",
            date_joined=date(2024, 1, 1),
            dept_name="Produce",
    
           
        )
        staff2 = Staff(
            first_name="Sarah",
            last_name="Wilson",
            username="swilson",
            password="staff456",
            date_joined=date(2024, 1, 15),
            dept_name="Inventory",
     
            
         
        )
        session.add_all([staff1, staff2])
        session.flush()

        # 3. Create Customer records (2)
        customer1 = Customer(
            first_name="Alice",
            last_name="Brown",
            username="abrown",
            password="cust123",
            cust_address="123 Main St",
            cust_balance=100.0,
            max_owing=500.0,
       
        )
        customer2 = Customer(
            first_name="Bob",
            last_name="Miller",
            username="bmiller",
            password="cust456",
            cust_address="456 Oak Ave",
            cust_balance=150.0,
       
            max_owing=750.0
        )
        session.add_all([customer1, customer2])
        session.flush()

        # 4. Create Corporate Customer records (2)
        corp1 = CorporateCustomer(
            first_name="James",
            last_name="Corp",
            username="jcorp",
            password="corp123",
            cust_address="789 Business Blvd",
            cust_balance=1000.0,
            max_owing=5000.0,
            discount_rate=0.15,
            max_credit=10000.0,
            min_balance=500.0
            
        )
        corp2 = CorporateCustomer(
            first_name="Lisa",
            last_name="Enterprise",
            username="lenterprise",
            password="corp456",
            cust_address="321 Commerce St",
            cust_balance=2000.0,
            max_owing=7500.0,
            discount_rate=0.20,
            max_credit=15000.0,
            min_balance=1000.0
        )
        session.add_all([corp1, corp2])
        session.flush()

        # 5. Create Veggie records (6)
        veggie1 = Veggie(id=1, vegName="Carrot")
        veggie2 = Veggie(id=2, vegName="Potato")
        veggie3 = Veggie(id=3, vegName="Tomato")
        veggie4 = Veggie(id=4, vegName="Cucumber")
        veggie5 = Veggie(id=5, vegName="Lettuce")  # 추가
        veggie6 = Veggie(id=6, vegName="Broccoli")  # 추가
        session.add_all([veggie1, veggie2, veggie3, veggie4, veggie5, veggie6])
        session.flush()

        # 6. Create WeightedVeggie records (2)
        weighted1 = WeightedVeggie(
            veggie_id=1,
            weight=2.5,
            weightPerKilo=1.5
        )
        weighted2 = WeightedVeggie(
            veggie_id=2,
            weight=3.0,
            weightPerKilo=2.0
        )
        session.add_all([weighted1, weighted2])
        session.flush()

        # 7. Create PackVeggie records (2)
        pack1 = PackVeggie(
            veggie_id=3,  # 이 ID는 위에서 생성한 Veggie의 ID와 일치해야 합니다
            numOfPack=5,
            pricePerPack=3.99
        )
        pack2 = PackVeggie(
            veggie_id=4,  # 이 ID는 위에서 생성한 Veggie의 ID와 일치해야 합니다
            numOfPack=3,
            pricePerPack=4.99
        )
        session.add_all([pack1, pack2])
        session.flush()


        # 8. Create UnitPriceVeggie records (2)
        unit1 = UnitPriceVeggie(
            veggie_id=5,
            pricePerUnit=0.99,
            quantity=10
        )
        unit2 = UnitPriceVeggie(
            veggie_id=6,
            pricePerUnit=1.49,
            quantity=8
        )
        session.add_all([unit1, unit2])
        session.flush()

        # 9. Create PremadeBox records (2)
        box1 = PremadeBox(
            id=7,
            boxSize="Small",
            numOfBoxes=10,
            vegName ="Premade",
            boxContent=[veggie1, veggie2, veggie3] , # 작은 박스에는 3가지 채소
  
        )
        box2 = PremadeBox(
            id=8,
            boxSize="Large",
            vegName ="Premade",
            numOfBoxes=5,
         
            boxContent=[veggie1, veggie2, veggie3, veggie4, veggie5]  # 큰 박스에는 5가지 채소
        )
        session.add_all([box1, box2])
        session.flush()


        

        # 12. Create CreditCardPayment records (2)
        credit1 = CreditCardPayment(
            payment_amount=100.0,
            payment_date=date(2024, 1, 22),
            payment_id="PAY001",
            customer_id=customer1.id,
            card_expiry_date=date(2025, 12, 31),
            card_number="4111111111111111",
            card_type="VISA",
             payment_method="credit_card",  #
        )
        credit2 = CreditCardPayment(
            payment_amount=200.0,
            payment_date=date(2024, 1, 23),
            payment_id="PAY002",
            customer_id=customer2.id,
            card_expiry_date=date(2026, 6, 30),
            card_number="5555555555554444",
            card_type="MasterCard",
             payment_method="credit_card",  #
        )
        session.add_all([credit1, credit2])
        session.flush()

        # 13. Create DebitCardPayment records (2)
        debit1 = DebitCardPayment(
            payment_amount=150.0,
            payment_date=date(2024, 1, 24),
            payment_id="PAY003",
            customer_id=customer1.id,
            bank_name="Bank of America",
             payment_method="debit_card",
            debit_card_number="4444333322221111"
        )
        debit2 = DebitCardPayment(
            payment_amount=250.0,
            payment_date=date(2024, 1, 25),
            payment_id="PAY004",
             payment_method="debit_card",
            customer_id=customer2.id,
            bank_name="Chase",
            debit_card_number="1111222233334444"
        )
        session.add_all([debit1, debit2])

        # Commit all changes
        session.commit()
        print("Successfully created mock data!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()
    finally:
        session.close()





if __name__ == "__main__":
 #
      create_mock_data()
    