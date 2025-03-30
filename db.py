import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to PostgreSQL with environment variable
DB_URL = os.getenv("DATABASE_URL")  

# Get all data from inventory
def fetch_inventory():

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # SQL query 
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()  

        # Closes resources 
        cur.close()
        conn.close()
        
        # Return the query data 
        return rows  

    # Error handling
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        return []

# Get all data from ledger   
def fetch_ledger():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # SQL query
        cur.execute("SELECT * FROM ledger")
        rows = cur.fetchall()  

        # Closes resources
        cur.close()
        conn.close()
        
        # Return the query data
        return rows  

    # Error Handling
    except Exception as e:
        print(f"Error fetching ledger: {e}")
        return []

# Add item to inventory   
def add_inventory_item(name, category, quantity, price):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Checks to see if item name already exists to prevent duplicate data
        cur.execute("SELECT COUNT(*) FROM inventory WHERE name = %s", (name,))
        count = cur.fetchone()[0]

        # Validation handling for an item with same name
        if count > 0:
            return "Item with this name already exists!"
        
        # Validation for quantity
        if quantity <= 0:
            return "Quantity must be greater than 0!"
        
        # Validation for price
        if price <= 0:
            return "Price must be greater than 0!"

        # Adds item to db
        cur.execute(
            """
            INSERT INTO inventory (name, category, quantity, price) 
            VALUES (%s, %s, %s, %s)
            RETURNING id, quantity, price
            """,
            (name, category, quantity, price)
        )

        # Adds transaction to ledger
        cur.execute(
            """
            INSERT INTO ledger (operation_type, item_name, category, previous_quantity, new_quantity, previous_price, new_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            ("INSERT", name, category, None, quantity, None, price)
        )

        # Commit the changes and close the resources
        conn.commit()
        cur.close()
        conn.close()
        return "Item added successfully!"
    
    # Error handling
    except Exception as e:
        return f"Error adding item: {e}"

# Update item 
def update_inventory_item(item_id, name, category, quantity, price):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Gets all the data from the requested item to update
        cur.execute("SELECT * FROM inventory WHERE id = %s", (item_id,))
        previous_entry = cur.fetchone()

        #if there is no previous entry, it will create a new entry in ledger with old price/quantity as 0.
        if not previous_entry:
            cur.execute(
                """
                INSERT INTO ledger (operation_type, item_name, category, previous_quantity, new_quantity, previous_price, new_price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                ("UPDATE", name, category, 0, quantity, 0, price)
            )
        else:
            # If there is a previous entry, use the data from previous_entry and add that data to ledger
            cur.execute(
                """
                INSERT INTO ledger (operation_type, item_name, category, previous_quantity, new_quantity, previous_price, new_price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                ("UPDATE", name, category, previous_entry[3], quantity, previous_entry[4], price)
            )

        # Update inventory with new data
        cur.execute(
            """
            UPDATE inventory 
            SET name = %s, category = %s, quantity = %s, price = %s 
            WHERE id = %s
            """,
            (name, category, quantity, price, item_id),
        )

        # Commit the changes and close the resources
        conn.commit()
        cur.close()
        conn.close()
        return "Item updated successfully!"
    
    # Error handling
    except Exception as e:
        return f"Error updating item: {e}"

# Delete Item
def delete_inventory_item(item_id):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Get the item to be deleted
        cur.execute("SELECT * FROM inventory WHERE id = %s", (item_id,))
        previous_entry = cur.fetchone()

        # Error handling for item not existing
        if not previous_entry:
            return f"Error: Item with ID {item_id} does not exist."
        
        # Add a transaction to ledger
        cur.execute(
            """
            INSERT INTO ledger (operation_type, item_name, category, previous_quantity, new_quantity, previous_price, new_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            ("DELETE", previous_entry[1], previous_entry[2], previous_entry[3], 0, previous_entry[4], 0)
        )

        # Delete the item from inventory
        cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))

        # Commit the changes and close reources
        conn.commit()
        cur.close()
        conn.close()
        return "Item deleted successfully!"
    
    # Error handling
    except Exception as e:
        return f"Error deleting item: {e}"

# Create tables for db
def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ledger (
            id SERIAL PRIMARY KEY,
            operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('INSERT', 'UPDATE', 'DELETE')),
            item_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            previous_quantity INTEGER,
            new_quantity INTEGER,
            previous_price DECIMAL(10,2),
            new_price DECIMAL(10,2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    # Connect to PostgreSQL and execute table creation
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Execute the creating the table
        for command in commands:
            cur.execute(command)

        # Commit the tables and close resources
        conn.commit()
        cur.close()
        conn.close()
        print("Tables created successfully!")

    # Error handling
    except Exception as e:
        print(f"Error: {e}")

# Run the script to create tables
if __name__ == "__main__":
    create_tables()