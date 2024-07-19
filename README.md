# E-Commerce Django Project

## Overview
This is a fully-functional e-commerce website built with Django, featuring a dynamic shopping cart system, user authentication, and a seamless checkout process. The project demonstrates the use of Django's powerful features along with modern web technologies to create a responsive and interactive online shopping experience.

## Features
- User Authentication (Register, Login, Logout)
- Product Catalog with Categories
- Dynamic Shopping Cart
- AJAX-powered Cart Operations (Add, Remove, Update Quantity)
- Checkout Process
- Order Management
- Admin Panel for Product and Order Management
- Responsive Design

## Technologies Used
- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **API**: Django Rest Framework (DRF)
- **AJAX**: jQuery for asynchronous operations
- **Version Control**: Git

## Setup and Installation
1. Clone the repository:
https://github.com/nexusameer/Multishop-Ecommerce
2. Navigate to the project directory:
cd ecommerce-django
3. Create a virtual environment:
pip install virtualenv
virtualenv myenv
4. Activate the virtual environment:
   .\myenv\Scripts\activate
5. Install the required packages:
pip install -r requirements.txt
6. Set up the database:
python manage.py migrate
7. Create a superuser:
python manage.py createsuperuser
8. Run the development server:
python manage.py runserver
