from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import sqlite3
from datetime import date
from flask import current_app as app

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    today = date.today()
    month = today.strftime('%Y-%m')
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        c.execute('''INSERT INTO budgets (user_id, category, amount, month) VALUES (?, ?, ?, ?)
                     ON CONFLICT(user_id, category, month) DO UPDATE SET amount=excluded.amount''',
                  (current_user.id, category, amount, month))
        conn.commit()
        flash('Budget updated!', 'success')
    c.execute('SELECT category, amount FROM budgets WHERE user_id = ? AND month = ?', (current_user.id, month))
    budgets = c.fetchall()
    conn.close()
    return render_template('budgets.html', budgets=budgets) 