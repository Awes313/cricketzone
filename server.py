from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import csv

app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect('back.db')
    c = conn.cursor()

    # Contact Messages Table
    c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')

    # Purchases Table
    c.execute('''CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_type TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    payment_mode TEXT NOT NULL
                )''')

    conn.commit()
    conn.close()

init_db()


# ---------- BASIC ROUTES ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bats')
def bats():
    return render_template('bats.html')

@app.route('/bowls')
def bowls():
    return render_template('bowls.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# ---------- BAT DETAILS ----------
@app.route('/bat1-details')
def bat1_details():
    return render_template('bat1-details.html')

@app.route('/bat2-details')
def bat2_details():
    return render_template('bat2-details.html')

@app.route('/bat3-details')
def bat3_details():
    return render_template('bat3-details.html')

@app.route('/bat4-details')
def bat4_details():
    return render_template('bat4-details.html')


# ---------- BOWL DETAILS ----------
@app.route('/bowl1-details')
def bowl1_details():
    return render_template('bowl1-details.html')

@app.route('/bowl2-details')
def bowl2_details():
    return render_template('bowl2-details.html')

@app.route('/bowl3-details')
def bowl3_details():
    return render_template('bowl3-details.html')

@app.route('/bowl4-details')
def bowl4_details():
    return render_template('bowl4-details.html')


# ---------- CONTACT FORM SUBMISSION ----------
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    reason = request.form['reason']
    message = request.form['message']

    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute("INSERT INTO contact_messages (name, email, reason, message) VALUES (?, ?, ?, ?)",
              (name, email, reason, message))
    conn.commit()
    conn.close()

    return redirect(url_for('thankyou', source='contact'))


# ---------- PURCHASE FORM ----------
@app.route('/purchase/<product_type>', methods=['GET'])
def purchase(product_type):
    bats = ["MRF Genius Grand Edition", "SS Ton Reserve Edition", "Gray-Nicolls Legend", "Kookaburra Kahuna Pro"]
    bowls = ["Kookaburra Leather Ball", "SG Test White Ball", "Cosco Practice Ball", "Nivia Wind Ball"]

    if product_type == 'bat':
        products = bats
    elif product_type == 'bowl':
        products = bowls
    else:
        products = []

    return render_template('purchase.html', product_type=product_type, products=products)


# ---------- PURCHASE FORM SUBMISSION ----------
@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    product_type = request.form['product_type']
    product_name = request.form['product_name']
    customer_name = request.form['customer_name']
    email = request.form['email']
    address = request.form['address']
    quantity = request.form['quantity']
    payment_mode = request.form['payment_mode']

    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute('''INSERT INTO purchases 
                 (product_type, product_name, customer_name, email, address, quantity, payment_mode)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (product_type, product_name, customer_name, email, address, quantity, payment_mode))
    conn.commit()
    conn.close()

    return redirect(url_for('thankyou', source='purchase'))


# ---------- ADMIN DASHBOARD ----------
@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('back.db')
    c = conn.cursor()

    c.execute("SELECT * FROM contact_messages")
    contact_data = c.fetchall()

    c.execute("SELECT * FROM purchases")
    purchase_data = c.fetchall()

    conn.close()
    return render_template('table.html', contact_data=contact_data, purchase_data=purchase_data)


# ---------- DELETE RECORDS ----------
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute("DELETE FROM contact_messages WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_purchase/<int:id>')
def delete_purchase(id):
    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute("DELETE FROM purchases WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


# ---------- EDIT CONTACT ----------
@app.route('/edit_contact/<int:id>')
def edit_contact(id):
    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contact_messages WHERE id = ?", (id,))
    contact = c.fetchone()
    conn.close()
    return render_template('edit_contact.html', contact=contact)

@app.route('/update_contact/<int:id>', methods=['POST'])
def update_contact(id):
    name = request.form['name']
    email = request.form['email']
    reason = request.form['reason']
    message = request.form['message']

    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute('''UPDATE contact_messages 
                 SET name=?, email=?, reason=?, message=? WHERE id=?''',
              (name, email, reason, message, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


# ---------- EDIT PURCHASE ----------
@app.route('/edit_purchase/<int:id>')
def edit_purchase(id):
    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute("SELECT * FROM purchases WHERE id = ?", (id,))
    purchase = c.fetchone()
    conn.close()
    return render_template('edit_purchase.html', purchase=purchase)

@app.route('/update_purchase/<int:id>', methods=['POST'])
def update_purchase(id):
    product_type = request.form['product_type']
    product_name = request.form['product_name']
    customer_name = request.form['customer_name']
    email = request.form['email']
    address = request.form['address']
    quantity = request.form['quantity']
    payment_mode = request.form['payment_mode']

    conn = sqlite3.connect('back.db')
    c = conn.cursor()
    c.execute('''UPDATE purchases 
                 SET product_type=?, product_name=?, customer_name=?, email=?, address=?, quantity=?, payment_mode=? 
                 WHERE id=?''',
              (product_type, product_name, customer_name, email, address, quantity, payment_mode, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))


# ---------- CSV DOWNLOAD ----------
@app.route('/download_csv/<table>')
def download_csv(table):
    conn = sqlite3.connect('back.db')
    c = conn.cursor()

    if table == 'contact':
        c.execute("SELECT * FROM contact_messages")
        rows = c.fetchall()
        headers = ['ID', 'Name', 'Email', 'Reason', 'Message']
        filename = 'contact_messages.csv'
    elif table == 'purchase':
        c.execute("SELECT * FROM purchases")
        rows = c.fetchall()
        headers = ['ID', 'Product Type', 'Product Name', 'Customer Name', 'Email', 'Address', 'Quantity', 'Payment Method']
        filename = 'purchase_orders.csv'
    else:
        return "Invalid table name"

    conn.close()

    response = make_response()
    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(rows)

    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response


# ---------- RUN SERVER ----------
if __name__ == '__main__':
    app.run(debug=True)
