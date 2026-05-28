
# Homedo – Household Services Management System

A web-based application for booking household services such as cleaning, plumbing, electrician work, and more.  
Built using Django (Python) with role-based dashboards for users, service providers, and admin.

---

## Project Badges

![Django](https://img.shields.io/badge/Django-Framework-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-Language-3776AB?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-7952B3?style=for-the-badge&logo=bootstrap)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen?style=for-the-badge)

---

## UI Screenshots

### Home Page
![Home Page](assests/screenshots/home.png)

---

### Booking Page
![Booking Page](assests/screenshots/booking.png)

---

### Dashboard
![Dashboard](assests/screenshots/homedo_dashboard.png)

---

### Profile Page
![Profile Page](assests/screenshots/homedo_profile.png)

---

### Services Page
![Services Page](assests/screenshots/services.png)

---

### Products Page
![Products Page](assests/screenshots/products.png)

---

### About Page
![About Page](assests/screenshots/homedo_about.png)

---

### Contact Page
![Contact Page](assests/screenshots/homedo_contact.png)

---

## Features

### Customer Panel

| Feature | Description |
|--------|-------------|
| Authentication | Secure login and registration |
| Service Booking | Book household services |
| Booking Status | Track Pending / Accepted / Declined |
| Payments | Razorpay and COD support |
| Order History | View previous bookings |

---

### Service Provider Panel

| Feature | Description |
|--------|-------------|
| View Requests | Incoming service bookings |
| Accept Booking | Approve requests |
| Decline Booking | Reject requests |
| Manage Services | Handle assigned tasks |

---

### Admin Panel

| Feature | Description |
|--------|-------------|
| User Management | Manage customers and providers |
| Service Management | Add, update, delete services |
| Booking Management | Monitor all bookings |
| Payment Tracking | View transactions |

---

## Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django (Python) |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Database | SQLite |
| Payment | Razorpay |
| Tools | VS Code, Git |

---

## System Flow

```

User → Login/Register → Browse Services → Book Service → Provider Accept/Decline → Payment → History

````

---

## Installation

```bash
git clone https://github.com/Harshali-14/Homedo-home-service-booking.git
cd Homedo-home-service-booking

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
````

---

## Payment System

| Method           | Status  |
| ---------------- | ------- |
| Razorpay         | Enabled |
| Cash on Delivery | Enabled |

---

## Modules

| Module         | Description                   |
| -------------- | ----------------------------- |
| Authentication | Login and registration system |
| Booking System | Service booking management    |
| Product System | Product ordering system       |
| Payment System | Transaction handling          |
| Admin Panel    | Full system control           |
| Provider Panel | Service provider dashboard    |

---

## Future Enhancements

| Feature             | Status  |
| ------------------- | ------- |
| Mobile Application  | Planned |
| Real-time Chat      | Planned |
| AI Recommendations  | Planned |
| Email Notifications | Planned |
| Analytics Dashboard | Planned |

---

## Developer

Harshali Kulkarni
MCA Student | Python and Django Developer
Pune, India

---

