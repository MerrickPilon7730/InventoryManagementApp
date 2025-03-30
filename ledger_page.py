import tkinter as tk
from tkinter import ttk
from db import fetch_ledger  # Ensure you have a function to fetch ledger data
from datetime import datetime

class LedgerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title for ledger page
        label = tk.Label(self, text="Ledger Page", font=("Arial", 14))
        label.pack(pady=10, padx=10, anchor="w")

        # Go to inventory button logic
        def go_to_inventory():
            from inventory_page import InventoryPage
            controller.show_frame(InventoryPage)

        # Go to inventory button
        button = tk.Button(self, text="Go to Inventory Page", command=go_to_inventory, bg="blue", fg="white", width=20)
        button.pack(pady=5, padx=10, anchor="w")

        # Ledger label
        label = tk.Label(self, text="Inventory Ledger", font=("Arial", 12))
        label.pack(pady=10, padx=10, anchor="w")

        # Create table
        self.tree = ttk.Treeview(self, columns=("Operation", "Item Name", "Category", "Prev Quantity", "New Quantity", "Previous Price", "New Price", "Date Modified"), show="headings")

        # Define column headings
        for col in ("Operation", "Item Name", "Category", "Prev Quantity", "New Quantity", "Previous Price", "New Price", "Date Modified"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        self.tree.pack(pady=10, padx=10, expand=True, fill="both")

        # Load ledger data
        self.load_ledger()

    # Load ledger data from db
    def load_ledger(self):

        # Fetch ledger data (fetch_ledger function is defined in db.py)
        data = fetch_ledger()

        # Sort data by id
        sorted_data = sorted(data, key=lambda item: item[0])  

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data into the table with formatted date
        for item in sorted_data:

            _, operation, item_name, category, prev_quantity, new_quantity, prev_price, new_price, date_modified = item

            # Convert timestamp to readable format (YYYY-MM-DD HH:MM:SS)
            try:
                formatted_date = datetime.strptime(str(date_modified), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Incase timestamp doesn't have microseconds
                formatted_date = datetime.strptime(str(date_modified), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

            # Insert data into table
            self.tree.insert("", "end", values=(operation, item_name, category, prev_quantity, new_quantity, prev_price, new_price, formatted_date))

    # Script to reload the data from db
    def refresh_ledger(self):
        self.load_ledger()

    # Script that overrides the tkraise function so every time the frame is brought to the front of the tk.Frame stack 
    # it not only loads the the frame but executes the refresh as well
    def tkraise(self, above_this=None):
        self.refresh_ledger()
        super().tkraise(above_this)