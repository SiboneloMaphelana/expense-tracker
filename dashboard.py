from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sqlite3
from datetime import date
from models import User
from flask import current_app as app

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    c.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (current_user.id,))
    total = c.fetchone()[0] or 0
    c.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 5', (current_user.id,))
    recent = c.fetchall()
    today = date.today()
    month_start = today.replace(day=1).strftime('%Y-%m-%d')
    month_end = today.strftime('%Y-%m-%d')
    month = today.strftime('%Y-%m')
    c.execute('SELECT SUM(amount), COUNT(*), AVG(amount) FROM expenses WHERE user_id = ? AND date >= ? AND date <= ?', (current_user.id, month_start, month_end))
    total_month, count_month, avg_month = c.fetchone()
    total_month = total_month or 0
    count_month = count_month or 0
    avg_month = avg_month or 0
    c.execute('SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? AND date >= ? AND date <= ? GROUP BY category ORDER BY total DESC LIMIT 1', (current_user.id, month_start, month_end))
    row = c.fetchone()
    top_category = row[0] if row else None
    c.execute('SELECT category, amount FROM budgets WHERE user_id = ? AND month = ?', (current_user.id, month))
    budgets = c.fetchall()
    budget_progress = []
    for cat, budget_amt in budgets:
        c.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ? AND date >= ? AND date <= ?', (current_user.id, cat, month_start, month_end))
        spent = c.fetchone()[0] or 0
        percent = (spent / budget_amt * 100) if budget_amt > 0 else 0
        budget_progress.append({'category': cat, 'budget': budget_amt, 'spent': spent, 'percent': percent})
    c.execute('SELECT SUM(amount) FROM incomes WHERE user_id = ? AND month = ?', (current_user.id, month))
    income_month = c.fetchone()[0] or 0
    conn.close()
    stats = {
        'total_month': total_month,
        'count_month': count_month,
        'avg_month': avg_month,
        'top_category': top_category,
        'income_month': income_month,
        'budget_progress': budget_progress
    }
    return render_template('index.html', total=total, recent=recent, stats=stats) 