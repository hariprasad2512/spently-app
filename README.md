# Spently - Personal Finance Tracker

Spently helps users log daily expenses, categorize them, and see an overview of their spending. It features a modern, tech-forward, and app-like feel designed for clean and rapid expense management.

## 🚀 Key Features

* **Secure User Authentication**: Users log in to see only their data.
* **Complete Expense Management**: Create, Read, Update, and Delete expense entries (Amount, Category, Date, Description).
* **Intelligent Dashboard**: Simple monthly total and filtering by category.
* **Data Visualization**: We will add simple charts (using Chart.js) to visually show spending by category.
* **Production Ready**: Configured with `whitenoise` for static files, `dj-database-url` for database switching, and `python-dotenv` for secret management.

## 🧰 Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Django views & models |
| **Frontend** | Django HTML Templates + Tailwind CSS / DaisyUI |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Charts** | Chart.js via CDN |

## 🛠️ Local Setup Instructions

1. Clone the repository to your local machine.
2. Create an isolated virtual environment: `python -m venv venv`
3. Activate the virtual environment. 
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory and add `SECRET_KEY=your_secret_key` and `DEBUG=True`.
6. Run database migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`
8. Visit `http://127.0.0.1:8000/` in your browser.

## ☁️ Deployment

It uses a straightforward relational database structure (perfect for PostgreSQL or SQLite), making it lightweight and easy to host on free or low-cost tiers.