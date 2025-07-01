from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import sqlite3
from datetime import date
from flask import current_app as app

incomes_bp = Blueprint('incomes', __name__)

@incomes_bp.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    today = date.today()
    month = today.strftime('%Y-%m')
    income_categories = ['Salary', 'Freelance', 'Investment', 'Gifts', 'Other']
    if request.method == 'POST':
        date_str = request.form['date']
        amount = float(request.form['amount'])
        description = request.form['description']
        category = request.form['category']
        c.execute('INSERT INTO incomes (user_id, date, amount, description, month, category) VALUES (?, ?, ?, ?, ?, ?)',
                  (current_user.id, date_str, amount, description, month, category))
        conn.commit()
        flash('Income added!', 'success')
    c.execute('SELECT date, amount, description, category FROM incomes WHERE user_id = ? AND month = ? ORDER BY date DESC', (current_user.id, month))
    incomes = c.fetchall()
    conn.close()
    return render_template('incomes.html', incomes=incomes, income_categories=income_categories) 