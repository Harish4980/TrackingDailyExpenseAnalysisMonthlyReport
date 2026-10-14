import sys
import os

# Add root project directory to sys.path so app and database modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel Serverless Function entry point
app = app

