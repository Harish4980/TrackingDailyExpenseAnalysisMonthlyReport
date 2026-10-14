# Daily Expense Tracker

A web-based personal finance management application built with Python and Flask. Track your daily expenses, monitor your monthly spending, and view visual category breakdowns.

## Features

- **User Authentication**: Secure user registration and login with email/phone.
- **Expense Management**: Add, update, and delete daily expenses with date, amount, category, and notes.
- **Categorization**: Organize expenses into categories like Food, Travel, Rent, Utilities, Entertainment, Healthcare, etc.
- **Dashboard Overview**: Quickly view today's total, monthly spending, and recent transactions.
- **Monthly Reports & Charts**: Visual breakdown of spending by category for any selected month.

## Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, Bootstrap / CSS3, JavaScript, Chart.js

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/TrackingDailyExpense.git
cd TrackingDailyExpense
```

### 2. Create and activate a virtual environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

## Deploying to Vercel

This repository is pre-configured for instant deployment on [Vercel](https://vercel.com):

1. Push your latest code to your GitHub repository.
2. Log in to [vercel.com](https://vercel.com) and click **"Add New..." > "Project"**.
3. Import your GitHub repository (`TrackingDailyExpenseAnalysisMonthlyReport`).
4. Keep the default settings and click **Deploy**.
5. Once deployment completes, Vercel gives you a live production URL!

> **Note on Serverless Storage**: Vercel functions run in an ephemeral serverless environment. On Vercel, the SQLite database is automatically maintained in `/tmp/expenses.db`. For permanent, cross-instance production persistence, connecting an external database service (like Neon Postgres, Supabase, or Turso) is recommended.

## Project Structure

```
TrackingDailyExpense/
│
├── api/
│   └── index.py        # Vercel serverless function entrypoint
├── app.py              # Main Flask application and routes
├── database.py         # SQLite database schema and queries
├── vercel.json         # Vercel routing and configuration
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── expenses.html
│   └── report.html
└── static/             # Static assets (CSS, JavaScript)
    ├── css/
    └── js/
```


