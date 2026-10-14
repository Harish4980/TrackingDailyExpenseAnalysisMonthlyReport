import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('VERCEL'):
    DATABASE_NAME = os.path.join('/tmp', 'expenses.db')
else:
    DATABASE_NAME = os.path.join(BASE_DIR, 'expenses.db')

def get_db_connection():
    db_dir = os.path.dirname(DATABASE_NAME)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    if not os.path.exists(DATABASE_NAME):
        init_db()
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_dir = os.path.dirname(DATABASE_NAME)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, email, phone, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, email, phone, password)
            VALUES (?, ?, ?, ?)
        ''', (username, email, phone, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def verify_user(login_identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users 
        WHERE (email = ? OR phone = ?) AND password = ?
    ''', (login_identifier, login_identifier, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, phone FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, username, email, phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users 
            SET username = ?, email = ?, phone = ?
            WHERE id = ?
        ''', (username, email, phone, user_id))
        conn.commit()
        success = True
        error_msg = None
    except sqlite3.IntegrityError:
        success = False
        error_msg = 'Email or phone number is already registered by another account.'
    finally:
        conn.close()
    return success, error_msg

def update_user_password(user_id, current_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    if not row or row['password'] != current_password:
        conn.close()
        return False, 'Current password is incorrect.'
    
    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
    conn.commit()
    conn.close()
    return True, 'Password changed successfully!'

def get_user_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    total_count = row[0]
    total_spent = row[1]
    
    cursor.execute('SELECT COUNT(DISTINCT category) FROM expenses WHERE user_id = ?', (user_id,))
    category_count = cursor.fetchone()[0]
    
    conn.close()
    return {
        'total_count': total_count,
        'total_spent': total_spent,
        'category_count': category_count
    }

def add_expense(user_id, title, amount, category, date, description=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (user_id, title, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, amount, category, date, description))
    conn.commit()
    conn.close()

def get_all_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC', (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_expense_by_id(expense_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
    expense = cursor.fetchone()
    conn.close()
    return expense

def update_expense(expense_id, user_id, title, amount, category, date, description=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE expenses
        SET title = ?, amount = ?, category = ?, date = ?, description = ?
        WHERE id = ? AND user_id = ?
    ''', (title, amount, category, date, description, expense_id, user_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
    conn.commit()
    conn.close()

def get_expenses_by_month(user_id, year_month_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM expenses 
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        ORDER BY date DESC, id DESC
    ''', (user_id, year_month_str))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_category_summary(user_id, year_month_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) as total_amount 
        FROM expenses 
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        GROUP BY category
        ORDER BY total_amount DESC
    ''', (user_id, year_month_str))
    summary = cursor.fetchall()
    conn.close()
    return summary

def get_total_spent_today(user_id):
    today = datetime.now().strftime('%Y-%m-%d')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date = ?', (user_id, today))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_total_spent_this_month(user_id):
    current_month = datetime.now().strftime('%Y-%m')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?", (user_id, current_month))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_recent_expenses(user_id, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?', (user_id, limit))
    expenses = cursor.fetchall()
    conn.close()
    return expenses