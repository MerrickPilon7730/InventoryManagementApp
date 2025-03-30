import tkinter as tk
from tkinter import ttk, messagebox
from db import fetch_inventory, add_inventory_item, update_inventory_item, delete_inventory_item
from datetime import datetime

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_item_id = None  

        # Page layout
        label = tk.Label(self, text="Inventory Page", font=("Arial", 14))
        label.pack(pady=10, padx=10, anchor="w")

        # Go to ledger button logic
        def go_to_ledger():
            from ledger_page import LedgerPage
            controller.show_frame(LedgerPage)

        # Go to ledger button
        button = tk.Button(self, text="Go to Ledger Page", command=go_to_ledger, bg="blue", fg="white", width=20)
        button.pack(pady=5, padx=10, anchor="w")

        # Manage inventory items label
        label = tk.Label(self, text="Manage Inventory Items", font=("Arial", 12))
        label.pack(pady=10, padx=10, anchor="w")

        # Form for managing inventory items
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        # Labels for input fields
        tk.Label(form_frame, text="Item Name:").grid(row=0, column=0)
        tk.Label(form_frame, text="Category:").grid(row=1, column=0)
        tk.Label(form_frame, text="Quantity:").grid(row=2, column=0)
        tk.Label(form_frame, text="Price:").grid(row=3, column=0)

        # Input fields
        self.name_entry = tk.Entry(form_frame)
        self.category_entry = tk.Entry(form_frame)
        self.quantity_entry = tk.Entry(form_frame)
        self.price_entry = tk.Entry(form_frame)

        # Grid for input fields
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button frame for Add, Update, and Delete buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)

        # Add Button
        add_button = tk.Button(button_frame, text="Add Item", command=self.add_item, bg="green", fg="white", width=15)
        add_button.pack(side=tk.LEFT, padx=5)

        # Update Button
        update_button = tk.Button(button_frame, text="Update Item", command=self.update_item, bg="orange", fg="white", width=15)
        update_button.pack(side=tk.LEFT, padx=5)

        # Delete Button
        delete_button = tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg="red", fg="white", width=15)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Clear Form Button
        delete_button = tk.Button(button_frame, text="Clear Form", command=self.clear_form, bg="gray", fg="white", width=15)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Inventory Items label
        label = tk.Label(self, text="Inventory Items", font=("Arial", 12))
        label.pack(pady=10, padx=10, anchor="w")

        # Create Table
        self.tree = ttk.Treeview(self, columns=("Id", "Item Name", "Category", "Quantity", "Price", "Date Added"), show="headings", height=25)

        # Define column headings
        for col in ("Id", "Item Name", "Category", "Quantity", "Price", "Date Added"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        # Pack table
        self.tree.pack(pady=10, padx=10, expand=True, fill="both")

        # Bind row selection
        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)

        # Load inventory data
        self.load_inventory()

    # Load inventory data from db
    def load_inventory(self):
        # Fetch inventory data (fetch_inventory function is defined in db.py)
        data = fetch_inventory()

        # Sort data by ID 
        sorted_data = sorted(data, key=lambda item: item[0])  

        # Clear existing data from table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data into the table with formatted date
        for item in sorted_data:
            item_id, name, category, quantity, price, date_added = item

            # Convert timestamp to readable format (YYYY-MM-DD HH:MM:SS)
            try:
                formatted_date = datetime.strptime(str(date_added), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Incase timestamp doesn't have microseconds 
                formatted_date = datetime.strptime(str(date_added), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

            # Insert data into table
            self.tree.insert("", "end", values=(item_id, name, category, quantity, price, formatted_date))

    # Handles selecting an item from the treeview
    def on_item_selected(self, event):

        # Get selected item
        selected = self.tree.selection()

        # If an item is selected place the values into the form
        if selected:
            item = self.tree.item(selected[0])["values"]
            if item:
                self.selected_item_id = item[0]  
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, item[1])
                self.category_entry.delete(0, tk.END)
                self.category_entry.insert(0, item[2])
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, item[3])
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, item[4])

    # Adds a new item
    def add_item(self):

        # Get input values from the form
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        # Validate input values
        if not name or not category or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Please enter valid values!")
            return

        # Add item to database (add_inventory_item function is defined in db.py)
        result = add_inventory_item(name, category, int(quantity), float(price))

        # Show success or error message in a message box
        if result == "Item added successfully!":
            self.load_inventory()
            self.clear_form()
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    # Updates the selected item
    def update_item(self):

        # Check if an item is selected when update button is pushed
        if not self.selected_item_id:
            messagebox.showerror("Error", "No item selected!")
            return

        # Get input values from the form
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        # Validate input values
        if not name or not category or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Please enter valid values!")
            return

        # Update item in database (update_inventory_item function is defined in db.py)
        result = update_inventory_item(self.selected_item_id, name, category, int(quantity), float(price))

        # Show success or error message in a message box
        if result == "Item updated successfully!":
            self.load_inventory()
            self.clear_form()
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    # Deletes the selected item
    def delete_item(self):

        # Check if an item is selected when delete button is pushed
        if not self.selected_item_id:
            messagebox.showerror("Error", "No item selected!")
            return

        # Delete item from database (delete_inventory_item function is defined in db.py)
        result = delete_inventory_item(self.selected_item_id)

        # Show success or error message in a message box
        if result == "Item deleted successfully!":
            self.load_inventory()
            self.clear_form()
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

    # Clears the input fields
    def clear_form(self):

        # Sets all input fields to empty
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.selected_item_id = None  
