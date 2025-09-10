import os
from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "invoices.db"
PDF_OUTPUT_DIR = BASE_DIR / "output" / "invoices"
FONT_DIR = BASE_DIR / "assets" / "fonts"
ICON_DIR = BASE_DIR / "assets" / "icons"

# === App Info ===
APP_NAME = "GC InvoiceGen"
APP_LOGO_PATH = BASE_DIR / 'assets' / 'icons' / 'icon.ico'
DEFAULT_SENDER = {
    "name": "Your Name",
    "address": "Your Address",
    "email": "contact@mail.com",
    "phone": "+91-0000000000"
}

# === UI Settings ===
WINDOW_SIZE = "900x600"
THEME = "light"  # Options: 'dark', 'light'
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#39b06a"
FONT_FAMILY = "Poppins"
FONT_PATH = FONT_DIR / "Poppins-Regular.ttf"

# === Invoice Defaults ===
DEFAULT_TAX_PERCENT = 0
DEFAULT_DISCOUNT_PERCENT = 0
CURRENCY_SYMBOL = "₹"
INVOICE_PREFIX = "INV"
STARTING_NUMBER = 10001
DATE_FORMAT = "%d-%m-%Y"


# === System ===
OPEN_COMMAND = "start" if os.name == "nt" else "open"
