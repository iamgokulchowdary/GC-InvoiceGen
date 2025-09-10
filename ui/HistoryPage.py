import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from config.settings import PDF_OUTPUT_DIR

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=10, fg_color='transparent')
        self.pack(padx=20, pady=10, fill="both", expand=True)

        self.app = app

        ctk.CTkLabel(self, text="📜 Invoice History", font=("Arial", 16)).pack(pady=10)

        # === Search Row ===
        search_row = ctk.CTkFrame(self, fg_color='transparent')
        search_row.pack(fill="x", padx=10, pady=5)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_row, textvariable=self.search_var, placeholder_text="Search by name or date")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", self.filter_history)

        # === Buttons ===
        self.search_button = ctk.CTkButton(search_row, text="Search", command=self.filter_history)
        self.search_button.pack(side="left", padx=(0, 10))

        self.refresh_button = ctk.CTkButton(search_row, text="Refresh", command=self.load_history)
        self.refresh_button.pack(side="left")

        # === Treeview ===
        style = ttk.Style()
        style.configure("History.Treeview", font=("Arial", 16), rowheight=32)
        style.configure("History.Treeview.Heading", font=("Arial", 18, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Name", "Total", "Date"),
            show="headings",
            style="History.Treeview"
        )
        self.tree.heading("ID", text="Invoice ID")
        self.tree.heading("Name", text="Customer Name")
        self.tree.heading("Total", text="Total ₹")
        self.tree.heading("Date", text="Date")

        self.tree.column("ID", width=80, anchor="w")
        self.tree.column("Name", width=180, anchor="w")
        self.tree.column("Total", width=100, anchor="w")
        self.tree.column("Date", width=120, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.open_invoice_pdf)

        self.load_history()

    
    def filter_history(self, event=None):
        query = self.search_var.get().strip().lower()
        if not query:
            return

        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            invoice_id = str(values[0]).lower()
            name = str(values[1]).lower()
            date = str(values[3])  # Format: YYYY-MM-DD

            match_id = query in invoice_id
            match_name = query in name
            match_date = (
                query == date.lower() or
                date.lower().startswith(query) or
                query in date.lower()
            )

            if match_id or match_name or match_date:
                self.tree.reattach(item, '', 'end')
            else:
                self.tree.detach(item)



    def load_history(self):
        from core.database import DB
        db = DB()
        invoices = db.get_all_invoices()

        self.tree.delete(*self.tree.get_children())
        for inv in invoices:
            self.tree.insert("", "end", values=(inv["id"], inv["name"], f"{inv['total']:.2f}", inv["date"]))

    def open_invoice_pdf(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        invoice_values = self.tree.item(item_id)["values"]
        invoice_id = invoice_values[0]  # Assuming first column is ID

        # Build path to PDF (adjust if your naming convention is different)
        pdf_path = PDF_OUTPUT_DIR / f"{invoice_id}.pdf"

        import os
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)  # Windows only
        else:
            self.app.search_frame.show_error_popup(f"Invoice PDF not found:\n{pdf_path}")
