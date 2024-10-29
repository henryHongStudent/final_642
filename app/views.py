from flask import Flask, request, render_template, redirect, url_for, session, flash
from app import app, db_session
from app.userModel import Customer, Person, CorporateCustomer, Staff, Item
from app.Controller import Controller

controller = Controller(db_session)

@app.route('/', methods=['GET'])
def home_page():
     return render_template('base.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == 'GET':
         return render_template('login.html')
     else:
         data = request.form
         username = data['username']
         password = data['password']
         result = controller.login(username, password)
         if result and isinstance(result, dict):
             session.update(result)
             flash("Logged in successfully",'success')
             return redirect(url_for('home_page'))
         else:
             flash('Invalid username or password. Please try again.', 'danger')
             return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    if controller.logout():
        session.clear()  # 세션을 완전히 지웁니다.
        flash("Logged out successfully", 'success')
    else:
        flash("An error occurred during logout", 'error')
    return redirect(url_for('home_page'))


@app.route('/detail/<int:user_id>', methods=['GET'])
def user_detail(user_id):
     if session:
        user = db_session.query(Person).filter(Person.id == user_id).first()
        return render_template('profile.html', user=user)
     else:
         return redirect(url_for('login'))

@app.route('/customers', methods=['GET'])
def customer_list():
     if session and session["type"] == "staff":
        customers = controller.get_all_customers()
        return render_template('customer_list.html', customers=customers)
     else:
         flash('You are not authorized to view this page.', 'danger')
         return redirect(url_for('home_page'))

@app.route('/items', methods=['GET', 'POST'])
def get_items():
        weighted_veggies = controller.get_weighted_veggies()
        unit_viggies = controller.get_unit_viggies()
        pack_veggies = controller.get_pack_veggies()
        premade_boxes = controller.get_premade_boxes()
        account_credit = controller.get_available_balance(session['id'])
        return render_template(
            'items.html',
            weighted_veggies=weighted_veggies,
            unit_viggies=unit_viggies,
            pack_veggies=pack_veggies,
            premade_boxes=premade_boxes,
            account_credit=account_credit
        )
  




@app.route('/place_order', methods=['POST', 'GET'])
def place_order_process():
    if not session:
        flash('Please log in to place an order.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return redirect(url_for('get_items'))  
    
    else:  
        data = request.form
        order = controller.place_order(session['id'], data)
        
        if order:
            flash('Order placed successfully!', "success")
            return redirect(url_for('home_page')) 
        else:
            flash('There was an error processing your order. Please try again.', "danger")
            return redirect(url_for('get_items'))  


@app.route('/orders/current', methods=['GET','POST'])
def current_order():
    if request.method == 'GET':
        if session and session["type"] == 'customer':
            user_id = session['id']
            current_order = controller.get_current_order(user_id)
            return render_template("current_order.html",current_order=current_order)  
        elif session and session["type"] =='staff':
            current_order=controller.all_current_orders()
            return render_template("staff_current_order.html",current_order=current_order)  
    else:
        order_id = request.form.getlist('order_id')
        result=controller.cancel_order(order_id)
        if result == True:
            flash('Order canceled successfully!','success')
            return redirect(url_for('current_order'))  
        else: 
            flash('Error occurred while canceling order!','danger')
            return redirect(url_for('current_order')) 
    
    
    
@app.route('/order/previous', methods=['GET'])
def previous_order():
    if session and session["type"] =='staff':
        previous_order=controller.all_previous_orders()
        return render_template("staff_previous_order.html",previous_order=previous_order) 
    
    
    elif session and session["type"] =='customer':
        user_id = session['id']
        previous_order = controller.get_previous_order(user_id)
        return render_template("previous_order.html",previous_order=previous_order)  

@app.route('/update/order', methods=['POST'])
def update_order_status():
    order_id = request.form.get('order_id')
    status = request.form.get('order_status')
    result = controller.update_order_status_to_database(order_id, status)
    if result == True:
        flash("Status updated successfully", "success")
        return redirect(url_for('current_order'))  
        
    else:
        flash("Error occurred while updating status", "danger")
        return redirect(url_for('current_order')) 

   

@app.route('/order/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    if 'user_id' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login')) 
    success = controller.cancel_order(order_id)
    flash("Order cancelled successfully","success")
    return render_template('order_cancelled.html', success=success)  

@app.route('/orders/previous', methods=['GET'])
def get_previous_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    orders = controller.view_previous_orders(session['user_id'])
    return render_template('previous_orders.html', orders=orders)  # Render previous orders list

@app.route('/customer/details', methods=['GET'])
def get_customer_details():
    if 'user_id' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login'))  # Redirect to login if not authorized

    customer = controller.view_customer_details(session['user_id'])
    return render_template('customer_details.html', customer=customer)  # Render customer details




@app.route('/admin/orders/current', methods=['GET'])
def get_all_current_orders():
    if 'user_id' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login'))  # Redirect to login if not authorized

    orders = controller.view_all_current_orders()
    return render_template('all_current_orders.html', orders=orders)  # Render current orders for staff

@app.route('/admin/orders/previous', methods=['GET'])
def get_all_previous_orders():
    if 'user_id' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login'))  # Redirect to login if not authorized

    orders = controller.view_all_previous_orders()
    return render_template('all_previous_orders.html', orders=orders)  # Render previous orders for staff



@app.route('/admin/customers', methods=['GET'])
def get_all_customers():
    if 'user_id' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login'))  # Redirect to login if not authorized

    customers = controller.view_all_customers()
    return render_template('all_customers.html', customers=customers)  # Render all customers





@app.route('/total_sales', methods=['GET'])
def get_total_sales():
    if request.method == 'GET':
        if not session or session['type'] == 'Customer':
            flash('You must be logged in as staff to view total sales.', 'error')
            return redirect(url_for('login'))
        else:
            weekly_sales = controller.generate_total_sales('week')
            monthly_sales = controller.generate_total_sales('month')
            yearly_sales = controller.generate_total_sales('year')
            popular_items = controller.view_popular_items()  # Add this line

        return render_template('total_sales.html', 
                               weekly_sales=weekly_sales, 
                               monthly_sales=monthly_sales, 
                               yearly_sales=yearly_sales,
                               popular_items=popular_items)  # Add popular_items here


@app.route('/admin/items/popular', methods=['GET'])
def get_popular_items():
    if 'user_id' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login'))  # Redirect to login if not authorized

    popular_items = controller.view_popular_items()
    return render_template('popular_items.html', popular_items=popular_items)  # Render popular items
