
📈 Stock Tracker Web App

A Django-based stock market tracking application that lets users monitor real-time stock data, manage their watchlist, and view quick quotes for any company.

🚀 Features

🔑 User Authentication (Sign up, Login, Logout)

📊 Personal Watchlist (Add, edit, delete stocks)

⏱️ Real-Time Stock Data (powered by Yahoo Finance via yfinance)

📰 Latest Market News (auto-switching news cards)

⚡ Quick Quote Section – enter a company ticker (e.g., AAPL, GOOG) and instantly see live price with profit/loss in green/red

🎨 Modern UI/UX with glassmorphism + sticky notes style

🛠️ Tech Stack

Backend: Django, Python

Frontend: HTML, CSS, Bootstrap

Database: SQLite (default, can be switched to PostgreSQL/MySQL)

APIs/Libraries:

yfinance → stock price data

Django Auth → user management

📷 Screenshots




⚙️ Installation

Clone the repository:

git clone https://github.com/your-username/stock-tracker.git
cd stock-tracker


Create & activate a virtual environment:

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Create a superuser (for Django Admin):

python manage.py createsuperuser


Start the development server:

python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

👤 Usage

Sign up / Log in to manage your personal watchlist.

Add stocks to your watchlist and track their real-time performance.

Quick Quote to instantly check the latest price of any company.

News section keeps you updated with rotating financial headlines.

📌 Notes

This project is for personal / portfolio use only.

Do not use or distribute without explicit permission.
