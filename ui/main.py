import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from config.settings import WINDOW_SIZE, APP_NAME, THEME, APP_LOGO_PATH

from core.inventory import InventoryManager

from ui.InvoicePage import SearchFrame, ItemsFrame, CustomerFrame
from ui.HistoryPage import HistoryFrame
from ui.StorePage import StoreFrame


def launch_app():
    ctk.set_appearance_mode(THEME)
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(APP_NAME)
    app.iconbitmap(APP_LOGO_PATH)
    app.geometry(WINDOW_SIZE)
    

    # One shared inventory for the whole app
    app.inventory = InventoryManager()

    app.tabview = ctk.CTkTabview(app)
    app.tabview.pack(fill="both", expand=True)

    

    # Create tabs
    billing_tab = app.tabview.add("Billing")
    history_tab = app.tabview.add("History")
    store_tab = app.tabview.add("Store")

    # Instantiate modular frames
    app.search_frame = SearchFrame(billing_tab, app, inventory=app.inventory, items_frame=None)
    app.items_frame = ItemsFrame(billing_tab, inventory=app.inventory)
    app.customer_frame = CustomerFrame(billing_tab)
    app.search_frame.items_frame = app.items_frame

    app.history_frame = HistoryFrame(history_tab, app)
    app.store_frame = StoreFrame(store_tab, app)

    app.mainloop()