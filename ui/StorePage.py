import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

class StoreFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=10)
        self.pack(padx=20, pady=10, fill="both", expand=True)

        self.app = app

        ctk.CTkLabel(self, text="🛒 Store Inventory", font=("Arial", 16)).pack(pady=10)

        # === Entry Row ===
        entry_row = ctk.CTkFrame(self)
        entry_row.pack(fill="x", padx=10, pady=5)

        self.name_var = ctk.StringVar()
        self.rate_var = ctk.StringVar()
        self.tax_var = ctk.StringVar()

        self.name_entry = ctk.CTkEntry(entry_row, textvariable=self.name_var, placeholder_text="Item Name")
        self.rate_entry = ctk.CTkEntry(entry_row, textvariable=self.rate_var, placeholder_text="Rate ₹")
        self.tax_entry = ctk.CTkEntry(entry_row, textvariable=self.tax_var, placeholder_text="Tax %")

        self.name_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.rate_entry.pack(side="left", padx=5)
        self.tax_entry.pack(side="left", padx=5)

        self.suggestion_popup = None
        self.name_entry.bind("<KeyRelease>", self.update_suggestions)
        self.name_entry.bind("<Down>", self.focus_suggestion_box)



        self.add_button = ctk.CTkButton(entry_row, text="Add / Update", command=self.add_or_update_item)
        self.add_button.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(entry_row, text="Refresh", command=self.load_items)
        self.refresh_button.pack(side="left")

        # === Keyboard shortcuts ===
        self.name_entry.bind("<KeyRelease>", self.update_suggestions)
        self.tax_entry.bind("<Return>", lambda e: (self.add_or_update_item(), "break")[1])



        # === Treeview ===
        style = ttk.Style()
        style.configure("Store.Treeview", font=("Arial", 16), rowheight=32)
        style.configure("Store.Treeview.Heading", font=("Arial", 18, "bold"))

        self.tree = ttk.Treeview(self, columns=("Name", "Rate", "Tax"), show="headings", style="Store.Treeview")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Rate", text="Rate ₹")
        self.tree.heading("Tax", text="Tax %")

        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Rate", width=100, anchor="center")
        self.tree.column("Tax", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_items()

    def clear_fields(self):
        self.name_var.set("")
        self.rate_var.set("")
        self.tax_var.set("")
        self.name_entry.focus_set()
        self.suggestion_box = None

    def add_or_update_item(self):
        name = self.name_var.get().strip()
        try:
            rate = float(self.rate_var.get())
            tax = float(self.tax_var.get())
        except ValueError:
            self.app.search_frame.show_error_popup("Please enter valid rate and tax.")
            return

        from core.database import DB
        db = DB()
        db.add_item(name, rate, tax)
        self.load_items()

    def load_items(self):
        from core.database import DB
        db = DB()
        self.tree.delete(*self.tree.get_children())

        cursor = db.conn.cursor()
        cursor.execute("SELECT name, rate, tax_percent FROM items ORDER BY name ASC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        
        self.clear_fields()

    def update_suggestions(self, event=None):
        query = self.name_var.get().strip().lower()
        if not query:
            self.destroy_suggestion_popup()
            return

        from core.database import DB
        db = DB()
        cursor = db.conn.cursor()
        cursor.execute("SELECT name FROM items WHERE LOWER(name) LIKE ?", (f"%{query}%",))
        matches = [row[0] for row in cursor.fetchall()]

        if not matches:
            self.destroy_suggestion_popup()
            return

        if self.suggestion_popup:
            self.suggestion_popup.destroy()

        self.suggestion_popup = tk.Toplevel(self)
        self.suggestion_popup.wm_overrideredirect(True)
        self.suggestion_popup.configure(bg="white")

        x = self.name_entry.winfo_rootx()
        y = self.name_entry.winfo_rooty() + self.name_entry.winfo_height()
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

        # self.suggestion_box.focus_set()
        self.suggestion_box.selection_set(0)

    def focus_suggestion_box(self, event=None):
        if self.suggestion_box and self.suggestion_box.size() > 0:
            self.suggestion_box.focus_set()
            self.suggestion_box.selection_clear(0, tk.END)
            self.suggestion_box.selection_set(0)
            return "break"


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
        self.name_var.set(name)
        self.destroy_suggestion_popup()

        from core.database import DB
        db = DB()
        item = db.get_item_by_name(name)
        if item:
            _, rate, tax = item
            self.rate_var.set(str(rate))
            self.tax_var.set(str(tax))

    def destroy_suggestion_popup(self):
        if self.suggestion_popup:
            self.suggestion_popup.destroy()
            self.suggestion_popup = None


    def on_suggestion_select(self, event=None):
        selection = self.suggestion_box.curselection()
        if not selection:
            return

        selected_name = self.suggestion_box.get(selection[0])
        self.name_var.set(selected_name)
        self.suggestion_box.pack_forget()

        from core.database import DB
        db = DB()
        item = db.get_item_by_name(selected_name)
        if item:
            _, rate, tax = item
            self.rate_var.set(str(rate))
            self.tax_var.set(str(tax))
