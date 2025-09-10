import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

class SearchFrame(ctk.CTkFrame):
    def __init__(self, master, app, inventory, items_frame):
        super().__init__(master, corner_radius=10)
        self.pack(padx=20, pady=(20, 10), fill="x")

        self.app = app
        self.inventory = inventory
        self.items_frame = items_frame

        # === Search Entry ===
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search item...")
        self.search_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # === Manual Entry Fields ===
        self.rate_entry = ctk.CTkEntry(self, placeholder_text="Rate")
        self.tax_entry = ctk.CTkEntry(self, placeholder_text="Tax %")
        self.qty_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.qty_entry.update()

        self.rate_entry.pack(side="left", padx=5)
        self.tax_entry.pack(side="left", padx=5)
        self.qty_entry.pack(side="left", padx=5)

        # === Buttons ===
        self.add_button = ctk.CTkButton(self, text="Add Item", command=self.add_item)
        self.add_button.pack(side="left", padx=10)

        self.generate_button = ctk.CTkButton(self, text="Generate Invoice", command=self.generate_invoice)
        self.generate_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.clear_all_fields)
        self.reset_button.pack(side="left", padx=10)

        self.remove_button = ctk.CTkButton(self, text="Remove", command=self.remove_selected_item)
        self.remove_button.pack(side="left", padx=10)

        # === Suggestion Popup ===
        self.suggestion_popup = None
        self.suggestion_box = None

        # === Keyboard Bindings ===
        for entry in [self.search_entry, self.rate_entry, self.tax_entry, self.qty_entry]:
            entry.bind("<Return>", self.handle_enter_key)

        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.search_entry.bind("<Down>", self.focus_suggestion_box)

    # === Suggestion Logic ===
    def update_suggestions(self, event=None):
        if event and event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape"):
            return

        query = self.search_entry.get().strip().lower()
        if not query:
            self.destroy_suggestion_popup()
            return

        matches = self.inventory.search_matches(query)
        if not matches:
            self.destroy_suggestion_popup()
            return

        if self.suggestion_popup:
            self.suggestion_popup.destroy()

        self.suggestion_popup = tk.Toplevel(self)
        self.suggestion_popup.wm_overrideredirect(True)
        self.suggestion_popup.configure(bg="white")

        x = self.search_entry.winfo_rootx()
        y = self.search_entry.winfo_rooty() + self.search_entry.winfo_height()
        self.suggestion_popup.geometry(f"300x150+{x}+{y}")

        self.suggestion_box = tk.Listbox(
            self.suggestion_popup,
            font=("Arial", 14),
            height=min(5, len(matches)),
            bg="white",
            activestyle="dotbox"
        )
        self.suggestion_box.pack(fill="both", expand=True)
        self.suggestion_box.bind("<<ListboxSelect>>", self.on_suggestion_select)
        self.suggestion_box.bind("<Return>", self.on_suggestion_enter)
        self.suggestion_box.bind("<Escape>", lambda e: self.destroy_suggestion_popup())

        for name in matches:
            self.suggestion_box.insert(tk.END, name)

        self.suggestion_box.selection_set(0)

    def focus_suggestion_box(self, event=None):
        try:
            if self.suggestion_box and self.suggestion_box.size() > 0:
                self.suggestion_box.focus_set()
                self.suggestion_box.selection_clear(0, tk.END)
                self.suggestion_box.selection_set(0)
                return "break"
        except tk.TclError:
            self.suggestion_box = None
            self.suggestion_popup = None

    def on_suggestion_enter(self, event=None):
        selection = self.suggestion_box.curselection()
        if selection:
            selected_name = self.suggestion_box.get(selection[0])
            self.apply_selected_item(selected_name)

    def on_suggestion_select(self, event=None):
        selection = self.suggestion_box.curselection()
        if not selection:
            return
        selected_name = self.suggestion_box.get(selection[0])
        self.apply_selected_item(selected_name)

    def apply_selected_item(self, name):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, name)
        self.destroy_suggestion_popup()

        item = self.inventory.search_item(name)
        if item:
            self.rate_entry.delete(0, tk.END)
            self.rate_entry.insert(0, str(item["rate"]))
            self.tax_entry.delete(0, tk.END)
            self.tax_entry.insert(0, str(item["tax"]))

    def destroy_suggestion_popup(self):
        if self.suggestion_popup:
            self.suggestion_popup.destroy()
            self.suggestion_popup = None
            self.suggestion_box = None

    # === Core Actions ===
    def handle_enter_key(self, event=None):
        self.add_item()
        self.search_entry.focus_set()
        self.clear_fields()

    def show_error_popup(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Input Error")
        popup.geometry("400x120")
        popup.grab_set()
        ctk.CTkLabel(popup, text=message, font=("Arial", 14)).pack(pady=20)
        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)

    def clear_fields(self):
        for entry in [self.search_entry, self.rate_entry, self.tax_entry, self.qty_entry]:
            entry.delete(0, tk.END)

    def remove_selected_item(self):
        selected = self.items_frame.tree.selection()
        if not selected:
            self.show_error_popup("Please select an item to remove.")
            return

        for item_id in selected:
            item_values = self.items_frame.tree.item(item_id)["values"]
            item_name = item_values[0]
            self.inventory.remove_item(item_name)

        self.items_frame.refresh_items()

    def add_item(self):
        try:
            name = self.search_entry.get().strip()
            rate = float(self.rate_entry.get())
            tax = float(self.tax_entry.get())
            qty = int(self.qty_entry.get())
        except ValueError:
            self.show_error_popup("Please enter valid rate, tax, and quantity.")
            return

        self.inventory.add_or_update_item(name, rate, tax, qty)
        self.items_frame.refresh_items()
        self.clear_fields()

    def clear_all_fields(self):
        self.inventory.clear_items()
        self.items_frame.refresh_items()
        self.app.customer_frame.clear_fields()
        self.clear_fields()

    def generate_invoice(self):
        customer_data = self.app.customer_frame.get_customer_data()
        items = self.inventory.get_linked_items()

        if not customer_data["name"] or not items:
            self.show_error_popup("Please enter customer details and add at least one item.")
            return

        from core.database import DB
        from core.pdf_generator import build_invoice_pdf
        from datetime import datetime

        db = DB()
        date_str = datetime.now().strftime("%Y-%m-%d")
        invoice_id = db.save_invoice(customer_data, items, date=date_str)
        build_invoice_pdf(invoice_id, customer_data, items, date_str)

        self.clear_all_fields()


class ItemsFrame(ctk.CTkFrame):
    def __init__(self, master, inventory):
        super().__init__(master, corner_radius=10)
        self.pack(padx=20, pady=10, fill="both", expand=True)

        self.inventory = inventory

        # === Treeview for Linked Items ===
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 14, 'bold'), rowheight=32)  # Row font
        style.configure("Custom.Treeview.Heading", font=("Arial", 16, "bold"))

        self.tree = ttk.Treeview(self, columns=("Name", "Rate", "Tax", "Qty", "Total"), show="headings", style="Custom.Treeview")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Rate", text="Rate")
        self.tree.heading("Tax", text="Tax %")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Total", text="Total ₹")

        self.tree.column("Name", width=180, anchor="w")
        self.tree.column("Rate", width=80, anchor="center")
        self.tree.column("Tax", width=80, anchor="center")
        self.tree.column("Qty", width=80, anchor="center")
        self.tree.column("Total", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=(10, 5))

        # === Total Amount Label ===
        self.total_label = ctk.CTkLabel(self, text="Total: ₹0.00", font=("Arial", 16))
        self.total_label.pack(pady=(0, 10), anchor="e", padx=10)

    def refresh_items(self):
        """Refresh the treeview with current linked items and update total."""
        self.tree.delete(*self.tree.get_children())
        total_amount = 0

        for item in self.inventory.get_linked_items():
            item_total = item["rate"] * item["quantity"] * (1 + item["tax"] / 100)
            total_amount += item_total
            self.tree.insert("", "end", values=(
                item["name"],
                item["rate"],
                item["tax"],
                item["quantity"],
                f"{item_total:.2f}"
            ))

        self.total_label.configure(text=f"Total: ₹{total_amount:.2f}")


class CustomerFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.pack(padx=20, pady=(10, 20), fill="x")

        ctk.CTkLabel(self, text="👤 Customer Details", font=("Arial", 16)).pack(pady=10)

        # === First Row: Name, Phone, Email ===
        row_frame = ctk.CTkFrame(self)
        row_frame.pack(fill="x", padx=10, pady=5)

        self.name_entry = ctk.CTkEntry(row_frame, placeholder_text="Name", width=200)
        self.phone_entry = ctk.CTkEntry(row_frame, placeholder_text="Phone", width=150)
        self.email_entry = ctk.CTkEntry(row_frame, placeholder_text="Email", width=200)

        self.name_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.phone_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.email_entry.pack(side="left", padx=5, fill="x", expand=True)

        # === Second Row: Address ===
        self.address_entry = ctk.CTkEntry(self, placeholder_text="Address")
        self.address_entry.pack(fill="x", padx=10, pady=5)

    def get_customer_data(self):
        return {
            "name": self.name_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "address": self.address_entry.get().strip()
        }

    def clear_fields(self):
        for entry in [self.name_entry, self.phone_entry, self.email_entry, self.address_entry]:
            entry.delete(0, tk.END)