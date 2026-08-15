# DB connection config
# config.py – Environment & Database Configuration
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "presta_loans"),
    "user": os.getenv("DB_USER", "analyst"),
    "password": os.getenv("DB_PASSWORD", ""),
}

APP_CONFIG = {
    "export_dir": "outputs/",
    "date_format": "%Y-%m-%d",
    "datetime_format": "%Y-%m-%d %H:%M:%S",
}
