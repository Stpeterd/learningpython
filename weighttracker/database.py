import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_name="weight_tracker.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def _create_tables(self):
        if not self.conn:
            print("Cannot create tables: no database connection.")
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS weight_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    weight REAL NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_averages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_start_date TEXT NOT NULL,
                    average_weight REAL NOT NULL,
                    entry_count INTEGER NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_weight_entry(self, date_str, weight):
        if not self.conn:
            print("Cannot add entry: no database connection.")
            return False
        try:
            self.cursor.execute("INSERT INTO weight_entries (date, weight) VALUES (?, ?)", (date_str, weight))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding weight entry: {e}")
            return False

    def get_weight_entries_for_week(self, start_date_str, end_date_str):
        if not self.conn:
            print("Cannot get entries: no database connection.")
            return []
        try:
            self.cursor.execute("SELECT date, weight FROM weight_entries WHERE date BETWEEN ? AND ? ORDER BY date ASC", (start_date_str, end_date_str))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting weight entries: {e}")
            return []

    def get_all_weight_entries(self):
        if not self.conn:
            print("Cannot get all entries: no database connection.")
            return []
        try:
            self.cursor.execute("SELECT date, weight FROM weight_entries ORDER BY date DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all weight entries: {e}")
            return []

    def get_average_weight_for_week(self, start_date_str, end_date_str):
        if not self.conn:
            print("Cannot get average: no database connection.")
            return 0.0
        try:
            self.cursor.execute("SELECT AVG(weight) FROM weight_entries WHERE date BETWEEN ? AND ?", (start_date_str, end_date_str))
            result = self.cursor.fetchone()[0]
            return result if result is not None else 0.0
        except sqlite3.Error as e:
            print(f"Error getting average weight: {e}")
            return 0.0

    def get_entry_count_for_week(self, start_date_str, end_date_str):
        if not self.conn:
            print("Cannot get entry count: no database connection.")
            return 0
        try:
            self.cursor.execute("SELECT COUNT(*) FROM weight_entries WHERE date BETWEEN ? AND ?", (start_date_str, end_date_str))
            result = self.cursor.fetchone()[0]
            return result if result is not None else 0
        except sqlite3.Error as e:
            print(f"Error getting entry count: {e}")
            return 0

    def add_weekly_average(self, week_start_date_str, average_weight, entry_count):
        if not self.conn:
            print("Cannot add weekly average: no database connection.")
            return False
        try:
            self.cursor.execute("INSERT INTO weekly_averages (week_start_date, average_weight, entry_count) VALUES (?, ?, ?)", (week_start_date_str, average_weight, entry_count))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding weekly average: {e}")
            return False

    def get_all_weekly_averages(self):
        if not self.conn:
            print("Cannot get all weekly averages: no database connection.")
            return []
        try:
            self.cursor.execute("SELECT week_start_date, average_weight, entry_count FROM weekly_averages ORDER BY week_start_date DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all weekly averages: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def __del__(self):
        self.close()


