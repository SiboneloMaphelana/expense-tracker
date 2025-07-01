Expense Tracker
A Flask-based web application for tracking personal finances, budgeting, and expense management.

Table of Contents
Features
Requirements
Installation
Usage
Project Structure
Contributing
Features
User authentication and account management
Expense tracking and categorization
Budget creation and management
Income tracking
Financial dashboard with insights
Responsive design
Requirements
Python 3.6+
Flask
Flask-Login
Flask-Bcrypt
SQLite3
Installation
Clone the repository:
git clone (https://github.com/SiboneloMaphelana/expense-tracker)
cd expense-tracker
Install dependencies:
pip install flask flask-login flask-bcrypt
Initialize the database:
python app.py
Usage
Start the application:
python app.py
Access the application in your web browser:
http://localhost:10000 if testing locally, remove the port and host in app.py file.
Register a new account and start tracking your expenses, setting budgets, and managing your finances.
Project Structure
The application follows a modular blueprint structure:

app.py: Main application file and configuration
models.py: Database models and initialization
auth.py: Authentication blueprint (login, register, logout)
expenses.py: Expense management blueprint
budgets.py: Budget management blueprint
incomes.py: Income tracking blueprint
dashboard.py: Dashboard and data visualization
templates/: HTML templates for the web interface
static/: Static files (CSS, JavaScript, images)
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.