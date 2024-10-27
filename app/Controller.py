from app.userModel import Item, Veggie, CreditCardPayment,DebitCardPayment,WeightedVeggie,Order,OrderLine, PackVeggie, UnitPriceVeggie,Payment, PremadeBox, Person, Staff, Customer
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app import db_session
from flask import session
from datetime import datetime
from datetime import datetime, timedelta
from sqlalchemy import func



class Controller:
    def __init__(self, db_session):
        self.db_session = db_session
        

    def login(self, username, password):
        try:
           user = db_session.query(Person).filter(Person.username == username, Person.password == password).first()
           if user:
                user_info = db_session.query(Person).filter(Person.id == user.id).first()
                result = Person.get_login_user_details( user_info)
                print("=========================================================================")
                
                print(result)

                print("=========================================================================")

           return  result

        except Exception as e:
            print(f"An error occurred during login: {str(e)}")
            return False
        finally:
            self.db_session.close()

        # ... (나머지 메서드들)

    def logout(self):
        try:
            session.clear()
            return True
        except Exception as e:
            print(f"An error occurred during logout: {str(e)}")
            return False
    def get_all_customers(self):
        try:
            # 데이터베이스에서 고객 목록 가져오기
            users = db_session.query(Person).filter(Person.type == 'customer').all()
            result = []
            
            if users:
                # 각 사용자에 대해 get_all_user() 메서드를 호출
                result = [user.get_all_user() for user in users]
            return result

        except Exception as e:
            print("=========================================================================")
            print(f"An error occurred during get_all_customer: {str(e)}")
            print("=========================================================================")
            
            return False
        finally:
            self.db_session.close()

    def get_available_balance(self, user_id):
        try:
            if not user_id:
                print("No user ID provided.")
                return None

            user = self.db_session.query(Person).join(Customer).filter(Person.id == user_id).first()
            if user:
                return {
                    'cust_balance': user.customer.cust_balance,
                    'max_owing': user.customer.max_owing
                }
            return None
        except Exception as e:
            print(f"An error occurred in fetching user balance: {str(e)}")
            return None
        finally:
            self.db_session.close()


            
            
    def get_weighted_veggies(self):
  
        try:
            weighted_veggies = self.db_session.query(Veggie, WeightedVeggie).join(WeightedVeggie, Veggie.id == WeightedVeggie.veggie_id).all()
            weighted_veggies_result = []
            for veggie, weighted in weighted_veggies:
                weighted_veggies_result.append({
                    'id': veggie.id,
                    'vegName': veggie.vegName,
                    'weight': weighted.weight,
                    'weightPerKilo': weighted.weightPerKilo
                })
            return weighted_veggies_result
        except Exception as e:
            print(f"An error occurred in fetching weighted veggies: {str(e)}")
            return None
        finally :
            self.db_session.close()
    def get_unit_viggies(self):
        try:
            unit_price_veggies = self.db_session.query(Veggie, UnitPriceVeggie).join(UnitPriceVeggie, Veggie.id == UnitPriceVeggie.veggie_id).all()
            unit_price_veggies_result = []
            for veggie, unit_price in unit_price_veggies:
                unit_price_veggies_result.append({
                    'id': veggie.id,
                    'vegName': veggie.vegName,
                    'pricePerUnit': unit_price.pricePerUnit,
                    'quantity': unit_price.quantity
                })
            return unit_price_veggies_result
        except Exception as e:
            print(f"An error occurred in fetching unit price veggies: {str(e)}")
            return None
        finally :
            self.db_session.close()
    def get_pack_veggies(self):
        try:
            packed_veggies = self.db_session.query(Veggie, PackVeggie).join(PackVeggie, Veggie.id == PackVeggie.veggie_id).all()
            packed_veggies_result = []
            for veggie, pack in packed_veggies:
                packed_veggies_result.append({
                    'id': veggie.id,
                    'vegName': veggie.vegName,
                    'numOfPack': pack.numOfPack,
                    'pricePerPack': pack.pricePerPack
                })
            return packed_veggies_result
        except Exception as e:
            print(f"An error occurred in fetching pack veggies: {str(e)}")
            return None
        finally :
            self.db_session.close()
    def get_premade_boxes(self):
        try:
            premade_boxes = self.db_session.query(PremadeBox).all()

            premade_boxes_result = []
            for box in premade_boxes:
                premade_boxes_result.append({
                    'id': box.id,
                    'boxSize': box.boxSize,
                    'numOfBoxes': box.numOfBoxes,
                    'boxContent': [veggie.vegName for veggie in box.boxContent],
                    'totalPrice': box.get_total_price()
                })
            return premade_boxes_result
        except Exception as e:
            print(f"An error occurred in fetching premade boxes: {str(e)}")
            return None
        finally:
            self.db_session.close()

    def get_item_by_id(self, item_id):
        try:
            item = self.db_session.query(Item).get(item_id)
            if item and item.price is not None:
                return item
            else:
                print(f"Item with ID {item_id} does not have a valid price.")
                return None
        except Exception as e:
            print(f"An error occurred in fetching item by ID: {str(e)}")
            return None




    def place_order(self, customer_id, items):
        # 세션 확인
        if not session:
            return None

        # 주문할 아이템 딕셔너리 생성
        order_items = {}
        for key, value in items.items():
            if key.startswith('item_'):
                item_id = int(key.split('_')[1])  # 'item_1' -> 1
                quantity = int(value)
                if quantity > 0:
                    order_items[item_id] = quantity

        # 주문 생성
        order = Order(
            order_customer=customer_id,
            order_date=datetime.now(),
            order_number=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            order_status='Pending'
        )

        # 주문을 데이터베이스에 추가
        self.db_session.add(order)
        self.db_session.flush()  # ID 생성을 위해 flush

        # 주문 라인 아이템 생성
        for item_id, quantity in order_items.items():
            if quantity > 0:
                order_line = OrderLine(
                    order_id=order.id,
                    item_id=item_id,
                    quantity=quantity
                )
                self.db_session.add(order_line)

        # 결제 정보 추출
        total_amount = items.get('total_price')
        payment_method = items.get('payment_method')
        card_expiry_date = items.get('card_expiry_date')
        card_number = items.get('card_number')
        card_type = items.get('card_type')

        # 결제 생성
        if payment_method == 'credit_card':
            payment = CreditCardPayment(
                payment_id=None,
                payment_date=datetime.now(),
                payment_amount=float(total_amount),
                payment_method=payment_method,
                customer_id=customer_id,
                card_expiry_date=datetime.strptime(card_expiry_date, '%Y-%m').date(),
                card_number=card_number,
                card_type=card_type
            )
        elif payment_method == 'debit_card':
            payment = DebitCardPayment(
                payment_id=None,
                payment_date=datetime.now(),
                payment_amount=float(total_amount),
                payment_method=payment_method,
                customer_id=customer_id,
                bank_name="Bank Name",
                debit_card_number=card_number
            )
        elif payment_method == 'account_charge':
            # 고객 정보 조회
            customer = self.db_session.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                print(f"Customer with ID {customer_id} not found.")
                return None

            # 주문 가능 여부 확인
            available_credit = customer.max_owing - customer.cust_balance
            if float(total_amount) > available_credit:
                print(f"Order rejected. Total amount ({total_amount}) exceeds available credit ({available_credit}).")
                return None

            # 주문 처리 및 고객 잔액 업데이트
            customer.cust_balance += float(total_amount)
            payment = Payment(
                payment_id=None,
                payment_date=datetime.now(),
                payment_amount=float(total_amount),
                payment_method=payment_method,
                customer_id=customer_id
            )

        
        
        self.db_session.add(payment)

    
        self.db_session.commit()

        # # 디버깅을 위한 출력
        # print("Order placed successfully!") 
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print("Order Items:")
        # print(order_items)
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print("Payment Details:")
        # print(f"Payment ID: {payment.payment_id}")
        # print(f"Payment Date: {payment.payment_date}")
        # print(f"Payment Amount: {payment.payment_amount}")
        # print(f"Payment Method: {payment.payment_method}")
        # print(f"Customer ID: {payment.customer_id}")
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print(f"Card Expiry Date: {card_expiry_date}")
        # print(f"Card Number: {card_number}")
        # print(f"Card Type: {card_type}")
        # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        return order

    
    def get_current_order(self, customer_id):
        current_order = []  # List to store each order's details

        try:
            # Join Order, OrderLine, Item, and Person to fetch all required info in one query
            order_query = (
                self.db_session.query(Order, OrderLine, Item, Person)
                .join(OrderLine, Order.id == OrderLine.order_id)
                .join(Item, OrderLine.item_id == Item.id)
                .join(Person, Order.order_person_id == Person.id)
                .filter(Order.order_person_id == customer_id, Order.order_status == 'Pending')
                .all()
            )

            if not order_query:
                return None

            # Dictionary to accumulate each unique order's details
            order_details = {}

            # Organize query results into order details
            for order, order_line, item, person in order_query:
                if order.id not in order_details:
                    order_details[order.id] = {
                        'order_id': order.id,  # Include order_id here
                        'order_number': order.order_number,
                        'order_date': order.order_date,
                        'order_status': order.order_status,
                        'customer_name': f"{person.first_name} {person.last_name}",
                        'items': [],
                        'total_order_price': 0  # Initialize total_order_price
                    }

                # Append item details for each order line
                item_total = item.get_price() * order_line.quantity
                order_details[order.id]['items'].append({
                    'vegName': item.vegName,
                    'quantity': order_line.quantity,
                    'price': item.get_price(),
                    'total_price': item_total
                })
                order_details[order.id]['total_order_price'] += item_total

            # Add each order to current_order list
            current_order = list(order_details.values())
            print("+++++++++++++++++++++++++++++++++++++++++++++")
            print(current_order)  # Print the current_order list for debugging purposes
            print("+++++++++++++++++++++++++++++++++++++++++++++")

            return current_order

        except Exception as e:
            print(f"An error occurred while fetching current order: {str(e)}")
            return None

        finally:
            self.db_session.close()

            
    
    def all_current_orders(self):
        try:
            # Fetch all pending orders
            orders = self.db_session.query(Order, Person).join(Person, Order.order_person_id == Person.id).filter(Order.order_status == 'Pending').all()

            current_orders = []

            for order, person in orders:
                # Fetch order lines for each order
                order_lines = self.db_session.query(OrderLine, Item).join(Item, OrderLine.item_id == Item.id).filter(OrderLine.order_id == order.id).all()

                order_details = {
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'order_date': order.order_date,
                    'order_status': order.order_status,
                    'customer_name': f"{person.first_name} {person.last_name}",
                    'customer_id': person.id,
                    'items': [],
                    'total_order_price': 0
                }
                for order_line, item in order_lines:
                    item_total = item.get_price() * order_line.quantity
                    order_details['items'].append({
                        'vegName': item.vegName,
                        'quantity': order_line.quantity,
                        'price': item.get_price(),
                        'item_total': item_total
                    })
                    order_details['total_order_price'] += item_total

                current_orders.append(order_details)
                print(current_orders)
            return current_orders

        except Exception as e:
            print(f"An error occurred while fetching all current orders: {str(e)}")
            return None

        finally:
           
            self.db_session.close()

    def get_previous_order(self, customer_id):
        previous_order = []  # List to store each order's details

        try:
            # Join Order, OrderLine, Item, and Person to fetch all required info in one query
            order_query = (
                self.db_session.query(Order, OrderLine, Item, Person)
                .join(OrderLine, Order.id == OrderLine.order_id)
                .join(Item, OrderLine.item_id == Item.id)
                .join(Person, Order.order_person_id == Person.id)
                .filter(Order.order_person_id == customer_id, Order.order_status == 'Completed')
                .all()
            )

            if not order_query:
                return None

            # Dictionary to accumulate each unique order's details
            order_details = {}
            
            # Organize query results into order details
            for order, order_line, item, person in order_query:
                if order.id not in order_details:
                    order_details[order.id] = {
                        'order_number': order.order_number,
                        'order_date': order.order_date,
                        'order_status': order.order_status,
                        'customer_name': f"{person.first_name} {person.last_name}",
                        'items': []
                    }

                # Append item details for each order line
                order_details[order.id]['items'].append({
                    'vegName': item.vegName,
                    'quantity': order_line.quantity,
                    'price': item.get_price(),
                    'total_price': item.get_price() * order_line.quantity
                })

            # Calculate total order price and add each order to current_order list
            for order_id, details in order_details.items():
                details['total_order_price'] = sum(
                    item['total_price'] for item in details['items']
                )
                previous_order.append(details)  # Append to the current_order list

            return previous_order

        except Exception as e:
            print(f"An error occurred while fetching current order: {str(e)}")
            return None

        finally:
            self.db_session.close()
            
    def all_previous_orders(self):
        try:
            # Fetch all completed orders
            orders = self.db_session.query(Order, Person).join(Person, Order.order_person_id == Person.id).filter(Order.order_status == 'Completed').all()

            previous_orders = []

            for order, person in orders:
                # Fetch order lines for each order
                order_lines = self.db_session.query(OrderLine, Item).join(Item, OrderLine.item_id == Item.id).filter(OrderLine.order_id == order.id).all()

                order_details = {
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'order_date': order.order_date,
                    'order_status': order.order_status,
                    'customer_name': f"{person.first_name} {person.last_name}",
                    'customer_id': person.id,
                    'items': [],
                    'total_order_price': 0
                }

                for order_line, item in order_lines:
                    item_total = item.get_price() * order_line.quantity
                    order_details['items'].append({
                        'vegName': item.vegName,
                        'quantity': order_line.quantity,
                        'price': item.get_price(),
                        'item_total': item_total
                    })
                    order_details['total_order_price'] += item_total

                previous_orders.append(order_details)

            return previous_orders

        except Exception as e:
            print(f"An error occurred while fetching previous orders: {str(e)}")
            return None

        finally:
            self.db_session.close()
            
    def cancel_order(self, order_id):
        try:
            # Fetch the order to be canceled
            order = self.db_session.query(Order).filter(Order.id == order_id).first()
            # Delete associated OrderLines
            self.db_session.query(OrderLine).filter(OrderLine.order_id == order_id).delete()
            # Delete the Order
            self.db_session.delete(order)
            # Commit the changes
            self.db_session.commit()
            return True

        except Exception as e:
            self.db_session.rollback()
            print(f"An error occurred while canceling the order: {str(e)}")
            return False

        finally:
            self.db_session.close()
            

    def update_order_status_to_database(self, order_id, status):
            try:
                # Fetch the order
                order = self.db_session.query(Order).filter(Order.id == order_id).first()
                
                if not order:
                    print(f"Order with id {order_id} not found.")
                    return False
                
                # Update the order status
                order.order_status = status
                
                # Commit the changes
                self.db_session.commit()
                
                print(f"Order status updated successfully for order {order_id}.")
                return True
        
            except Exception as e:
                self.db_session.rollback()
                print(f"An error occurred while updating the order status: {str(e)}")
                return False
        
            finally:
                self.db_session.close()

    def generate_total_sales(self, period):
        try:
            now = datetime.now()
            if period == 'week':
                start_date = now - timedelta(days=7)
                date_format = "%Y-%m-%d"  # 년-월-일
            elif period == 'month':
                start_date = now.replace(day=1)
                date_format = "%Y-%m"  # 년-월
            elif period == 'year':
                start_date = now.replace(month=1, day=1)
                date_format = "%Y"  # 년
            else:
                raise ValueError("Invalid period. Use 'week', 'month', or 'year'.")

            total_sales = (
                self.db_session.query(func.sum(Payment.payment_amount))
                .join(Order, Payment.id == Order.id)
                .filter(Order.order_status == 'Completed')
                .filter(Order.order_date >= start_date)
                .filter(Order.order_date <= now)
                .scalar()
            )

            return {
                'period': period,
                'start_date': start_date.strftime(date_format),
                'end_date': now.strftime(date_format),
                'total_sales': total_sales or 0
            }

        except Exception as e:
            print(f"An error occurred while generating total sales: {str(e)}")
            return None

        finally:
            self.db_session.close()

    

    def view_popular_items(self):
        # Query to get the sum of quantities for each item
        popular_items = self.db_session.query(
            Item.vegName,
            func.sum(OrderLine.quantity).label('total_quantity')
        ).join(OrderLine, Item.id == OrderLine.item_id)\
         .group_by(Item.id)\
         .order_by(func.sum(OrderLine.quantity).desc())\
         .limit(10)\
         .all()

        # Convert the result to a list of dictionaries
        result = [
            {"name": item.vegName, "sales_count": item.total_quantity}
            for item in popular_items
        ]

        return result