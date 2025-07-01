from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import sqlite3
from models import User
from flask import current_app as app

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        conn = sqlite3.connect(app.config['DB_NAME'])
        c = conn.cursor()
        c.execute('INSERT INTO expenses (user_id, date, description, amount, category) VALUES (?, ?, ?, ?, ?)',
                  (current_user.id, date, description, amount, category))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard.index'))
    return render_template('add.html')

@expenses_bp.route('/expenses', methods=['GET', 'POST'])
@login_required
def list_expenses():
    filter_query = 'WHERE user_id = ?'
    params = [current_user.id]
    if request.method == 'POST':
        category = request.form.get('category')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if category:
            filter_query += ' AND category = ?'
            params.append(category)
        if start_date:
            filter_query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            filter_query += ' AND date <= ?'
            params.append(end_date)
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    c.execute(f'SELECT * FROM expenses {filter_query} ORDER BY date DESC, id DESC', params)
    expenses = c.fetchall()
    conn.close()
    return render_template('list.html', expenses=expenses)

@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    c.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, current_user.id))
    expense = c.fetchone()
    if not expense:
        conn.close()
        flash('Expense not found.', 'danger')
        return redirect(url_for('expenses.list_expenses'))
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        c.execute('UPDATE expenses SET date = ?, description = ?, amount = ?, category = ? WHERE id = ? AND user_id = ?',
                  (date, description, amount, category, expense_id, current_user.id))
        conn.commit()
        conn.close()
        flash('Expense updated!', 'success')
        return redirect(url_for('expenses.list_expenses'))
    conn.close()
    return render_template('edit.html', expense=expense)

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    conn = sqlite3.connect(app.config['DB_NAME'])
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, current_user.id))
    conn.commit()
    conn.close()
    flash('Expense deleted!', 'success')
    return redirect(url_for('expenses.list_expenses')) 