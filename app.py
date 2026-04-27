from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import os, time
from openai import OpenAI
client = OpenAI(api_key="openai")
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gaurav@4050",
    database="agro_market"
)
cursor = db.cursor(buffered=True)

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO users_data (username,password,role) VALUES (%s,%s,%s)",
            (request.form['username'],request.form['password'],request.form['role'])
        )
        db.commit()
        return redirect('/login')
    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cursor.execute(
            "SELECT * FROM users_data WHERE username=%s AND password=%s",
            (request.form['username'],request.form['password'])
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            return redirect('/home')

    return render_template('login.html')

# ---------------- USER HOME ----------------
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM products_data")
    products = cursor.fetchall()
    return render_template('user_home.html', products=products)

# ---------------- BUY ----------------
@app.route('/buy/<int:id>')
def buy(id):
    if session.get('role') != 'consumer':
        return redirect('/home')

    cursor.execute("SELECT stock FROM products_data WHERE id=%s",(id,))
    result = cursor.fetchone()

    if result:
        if result[0] > 1:
            cursor.execute("UPDATE products_data SET stock=stock-1 WHERE id=%s",(id,))
        else:
            cursor.execute("DELETE FROM products_data WHERE id=%s",(id,))
        db.commit()

    return redirect('/home')

# ---------------- SELL ----------------
@app.route('/sell', methods=['GET','POST'])
def sell():
    if session.get('role') != 'farmer':
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = str(int(time.time())) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cursor.execute(
                "INSERT INTO products_data (user_id,name,price,stock,image) VALUES (%s,%s,%s,%s,%s)",
                (session['user_id'],request.form['name'],request.form['price'],request.form['stock'],filename)
            )
            db.commit()

        return redirect('/home')

    return render_template('sell.html')



# ---------------- UPDATE ----------------
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    cursor.execute("SELECT * FROM products_data WHERE id=%s",(id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute(
            "UPDATE products_data SET name=%s,price=%s,stock=%s WHERE id=%s",
            (request.form['name'],request.form['price'],request.form['stock'],id)
        )
        db.commit()
        return redirect('/home')

    return render_template('update.html', product=product)

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username']=="admin" and request.form['password']=="1234":
            session['role']='admin'
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error="❌ Invalid Login")
    return render_template('admin_login.html')

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin')
def admin():
    if session.get('role')!='admin':
        return redirect('/')

    cursor.execute("SELECT * FROM products_data")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM users_data")
    users = cursor.fetchall()

    return render_template('admin_dashboard.html', products=products, users=users)

# ---------------- ADMIN ADD PRODUCT ----------------
@app.route('/admin_add', methods=['GET','POST'])
def admin_add():
    if request.method == 'POST':
        file = request.files['image']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cursor.execute(
                "INSERT INTO products_data (user_id,name,price,stock,image) VALUES (%s,%s,%s,%s,%s)",
                (0,request.form['name'],request.form['price'],request.form['stock'],filename)
            )
            db.commit()

        return redirect('/admin')

    return render_template('admin_add.html')

# ---------------- DELETE PRODUCT ----------------
@app.route('/admin_delete/<int:id>')
def admin_delete(id):
    cursor.execute("DELETE FROM products_data WHERE id=%s",(id,))
    db.commit()
    return redirect('/admin')

# ---------------- DELETE USER ----------------
@app.route('/delete_user/<int:id>')
def delete_user(id):
    cursor.execute("DELETE FROM users_data WHERE id=%s",(id,))
    db.commit()
    return redirect('/admin')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
