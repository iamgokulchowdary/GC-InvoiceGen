import sqlite3
from config.settings import DB_PATH

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                rate REAL NOT NULL,
                tax_percent REAL NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                date TEXT,
                total_amount REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                item_name TEXT,
                rate REAL,
                tax_percent REAL,
                quantity INTEGER,
                FOREIGN KEY(invoice_id) REFERENCES invoices(id)
            )
        """)
        self.conn.commit()

    def add_item(self, name, rate, tax_percent):
        self.cursor.execute("""
            INSERT INTO items (name, rate, tax_percent)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                rate = excluded.rate,
                tax_percent = excluded.tax_percent
        """, (name, rate, tax_percent))
        self.conn.commit()
        

    def get_item_by_name(self, name):
        self.cursor.execute(
            "SELECT name, rate, tax_percent FROM items WHERE name = ?",
            (name,)
        )
        return self.cursor.fetchone()

    def save_invoice(self, customer, items, date):
        # Calculate total
        total = sum(
            item["rate"] * item["quantity"] * (1 + item["tax"] / 100)
            for item in items
        )

        # Save invoice
        self.cursor.execute("""
            INSERT INTO invoices (customer_name, phone, email, address, date, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer["name"],
            customer["phone"],
            customer["email"],
            customer["address"],
            date,
            total
        ))
        invoice_id = self.cursor.lastrowid

        # Save linked items
        for item in items:
            self.cursor.execute("""
                INSERT INTO invoice_items (invoice_id, item_name, rate, tax_percent, quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (
                invoice_id,
                item["name"],
                item["rate"],
                item["tax"],
                item["quantity"]
            ))

        self.conn.commit()
        return invoice_id

    def get_all_invoices(self):
        self.cursor.execute("""
            SELECT id, customer_name, total_amount, date
            FROM invoices
            ORDER BY date DESC
        """)
        rows = self.cursor.fetchall()
        return [
            {"id": r[0], "name": r[1], "total": r[2], "date": r[3]}
            for r in rows
        ]
