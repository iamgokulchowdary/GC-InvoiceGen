
# 🧾 GC InvoiceGen — Project Overview

GC InvoiceGen is a desktop application built to streamline the process of generating professional invoices for small businesses, freelancers, or service providers. It combines a clean, tabbed user interface with a modular backend architecture to offer a fast, intuitive, and customizable billing experience.

---

## 🧠 Purpose & Philosophy

The project was designed with three core principles:

1. **Modularity**: Every component—from UI frames to database logic—is isolated and reusable. This makes the system easy to maintain, extend, or refactor.
2. **Centralized Configuration**: All constants, paths, UI settings, and invoice defaults are defined in a single `settings.py` file. This ensures consistency and simplifies customization.
3. **Real-World Utility**: The app handles practical edge cases like item updates, tax calculations, and PDF generation with sender/customer metadata—making it suitable for actual business use.

---

## 🖥️ User Interface

The application uses a tabbed layout with three main sections:

- **Billing Tab**: Users can search for items, manually enter rate/tax/quantity, and link them to an invoice. Customer details are entered alongside, and a single click generates a styled PDF invoice.
- **History Tab**: Displays previously generated invoices in a searchable table. Users can double-click any entry to open the corresponding PDF.
- **Store Tab**: Allows users to add or update inventory items with rate and tax details. Live search suggestions help avoid duplicates and speed up entry.

Each tab is backed by its own modular frame, and all UI elements are styled with custom fonts, icons, and consistent spacing for a polished look.

---

## 🧾 Invoice Generation Logic

Invoices are generated using the ReportLab library. The PDF includes:

- Sender and customer information
- Itemized table with rate, tax %, tax amount, quantity, and total
- Summary section with subtotal, total tax, and final amount
- Optional notes section

The layout is designed to be clean and printable, with subtle styling like shaded headers and aligned columns.

---

## 🗃️ Data Handling

All data is stored locally using SQLite. The database includes three tables:

- `items`: Stores inventory with name, rate, and tax
- `invoices`: Stores invoice metadata (customer info, date, total)
- `invoice_items`: Stores item-level details linked to each invoice

The app uses conflict-handling logic to update items if they already exist, and ensures referential integrity between invoices and their items.

---

## 🔄 Workflow Integration

The app maintains a shared `InventoryManager` instance across tabs, allowing seamless data flow between item search, invoice creation, and store updates. This avoids duplication and ensures that all actions reflect the latest state of the inventory.

Keyboard shortcuts, live suggestions, and error popups are integrated throughout the UI to enhance speed and usability.

---

## ✨ Key Features Explained
### 🧾 Invoice Creation
Live Item Search with Suggestions Type in an item name and get instant suggestions from your inventory. Speeds up entry and prevents duplicates.

Manual Entry Support You can override suggestions and manually enter rate, tax %, and quantity—ideal for one-off services or custom pricing.

Customer Details Capture Name, phone, email, and address fields are built into the billing flow. These are embedded into the final invoice PDF.

PDF Generation with Styling Invoices are generated using ReportLab with structured tables, sender/customer info, and a summary section. Designed to be print-ready and professional.

### 📜 Invoice History
Searchable Invoice Log View all past invoices in a sortable table. Search by customer name, invoice ID, or date.

Quick PDF Access Double-click any invoice entry to instantly open its PDF. No need to dig through folders.

### 🛒 Inventory Management
Add / Update Items Enter item name, rate, and tax % to populate your store. Existing items are updated automatically.

Live Suggestions While Typing As you type an item name, matching entries appear in a dropdown. Select to auto-fill rate and tax.

Treeview Display All items are shown in a styled table with columns for name, rate, and tax—easy to scan and verify.

### 🔄 Shared State Across Tabs
A single InventoryManager instance is shared across Billing, History, and Store tabs. This ensures consistency and avoids redundant data handling.

### 🧠 Smart UX Touches
Keyboard Shortcuts Press Enter to add items, navigate suggestions with arrow keys, and use Return to confirm selections.

Error Popups Invalid inputs trigger clean, modal popups with helpful messages—no silent failures.

Reset & Remove Buttons Clear all fields or remove selected items with a single click. Keeps the workflow fast and tidy.

### ⚙️ Configurable Defaults
All UI settings, invoice formatting rules, and sender info are defined in settings.py. You can change:

- Theme (light/dark)

- Font family and path

- Currency symbol

- Invoice prefix and starting number

- Default tax and discount rates


## 🎯 Why It Matters

GC InvoiceGen isn’t just a demo—it’s a practical tool built with real-world constraints in mind. It’s ideal for users who need:

- A fast way to generate invoices without relying on web apps
- Local data storage for privacy and offline access
- Customizable branding via fonts, icons, and themes
- A modular codebase that can be extended for GST, multi-currency, or analytics

Whether you're a solo entrepreneur or building a larger invoicing system, this project offers a solid foundation with thoughtful design choices and clean separation of concerns.
