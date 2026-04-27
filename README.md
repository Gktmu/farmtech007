# 🌾 Smart Agro Market — Farmer Marketplace System

## 📌 Project Overview

**Smart Agro Market** is a web-based platform that connects **farmers and consumers directly**.
It allows farmers to sell their products online and consumers to purchase fresh produce easily.

The system ensures:

* Direct farmer-to-customer interaction
* Fair pricing
* Simple and efficient digital marketplace

---

## 🚀 Features

### 👤 User Features

* User Registration & Login
* Role-based access (**Farmer / Consumer / Admin**)
* Browse products in a modern UI
* Buy products instantly

### 🌾 Farmer Features

* Add (Sell) products with image upload
* Update product details
* Manage stock

### 🛒 Consumer Features

* View all available products
* Purchase products easily

### 👑 Admin Features

* Admin dashboard
* Add/Delete products
* Manage users

---

## 🧠 Technologies Used

### Frontend

* HTML5
* CSS3 (Modern Green Theme + Responsive UI)
* JavaScript

### Backend

* Python (Flask Framework)

### Database

* MySQL

---

## 📁 Project Structure

```
SmartAgro/
│
├── static/
│   ├── uploads/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── user_home.html
│   ├── products.html
│   ├── sell.html
│   ├── update.html
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── admin_add.html
│
├── app.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/smart-agro.git
cd smart-agro
```

### 2️⃣ Install Dependencies

```bash
pip install flask mysql-connector-python
```

### 3️⃣ Setup Database

Create MySQL database:

```sql
CREATE DATABASE agro_market;
```

### Create Tables:

```sql
CREATE TABLE users_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(20)
);

CREATE TABLE products_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100),
    price INT,
    stock INT,
    image VARCHAR(255)
);
```

---

### 4️⃣ Run Application

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000/
```

---

## 📊 Future Enhancements

* 🛒 Add to Cart system
* 📦 Order tracking
* 📍 Location-based services
* 📊 Advanced analytics dashboard
* 📱 Mobile app version

---

## 🎯 Use Case

This system helps:

* Farmers sell products directly
* Consumers get fresh produce
* Improve transparency in agricultural markets

---

## 👨‍💻 Developed By

**Gaurav Kumar**
BCA Final Year Project

---

## ⭐ Conclusion

Smart Agro Market is a practical solution for modern agriculture, combining:

* E-commerce functionality
* Farmer empowerment
* Simple and efficient user experience

---

## 📌 License

This project is for educational purposes.
