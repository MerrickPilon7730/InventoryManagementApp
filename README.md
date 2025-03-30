# Inventory Management System

## Overview
This is a **Python-based Inventory Management System** with a **Tkinter GUI** and a **PostgreSQL database (hosted on Neon.tech)**. It allows users to perform CRUD operations on inventory items while maintaining a ledger for tracking changes.

## Features
- Add, update, and delete inventory items.
- Track inventory changes in a ledger.
- View inventory and ledger data in a Tkinter-based GUI.
- PostgreSQL database integration.
- Automatically logs added items, updates and deletions in the ledger.

## Technologies Used
- **Python** (Tkinter for GUI)
- **PostgreSQL** (Hosted on Neon.tech)
- **psycopg2** (for database connection)
- **pgAdmin** (for database management)

## Setup Instructions
### 1. Install Dependencies
Ensure you have Python installed (>=3.8). Then, install required dependencies:
```sh
pip install -r requirements.txt
```

### 2. Configure Database Connection
- Create a **.env** file in the project directory.
- Add your **Neon.tech PostgreSQL database URL** in the `.env` file:
  ```
  DB_URL=postgresql://your_username:your_password@your_host/your_database
  ```

### 3. Setup Database
Run the provided SQL script to create necessary tables:
```sh
psql -h <your_host> -U <your_user> -d <your_db> -f schema.sql
```
Alternatively, use **pgAdmin** to execute the `Assignment3SQL.sql` script.

### 4. Run the Application
```sh
python main.py
```

## Database Schema
The database consists of two tables:
### **inventory**
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique item identifier |
| name | VARCHAR(255) | Item name |
| category | VARCHAR(255) | Item category |
| quantity | INT | Available stock |
| price | DECIMAL(10,2) | Price per unit |
| date_added | TIMESTAMP DEFAULT NOW() | Timestamp of entry |

### **ledger**
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique ledger entry ID |
| operation_type | VARCHAR(10) | 'ADD', 'UPDATE', or 'DELETE' |
| item_name | VARCHAR(255) | Name of the item affected |
| category | VARCHAR(255) | Category of the item |
| previous_quantity | INT | Quantity before operation |
| new_quantity | INT | Quantity after operation |
| previous_price | DECIMAL(10,2) | Price before operation |
| new_price | DECIMAL(10,2) | Price after operation |
| date_modified | TIMESTAMP DEFAULT NOW() | Timestamp of operation |

## Usage
- **Adding an Item:** Fill in item details and click `Add Item`.
- **Updating an Item:** Select an item, edit fields, and click `Update Item`.
- **Deleting an Item:** Select an item and click `Delete Item`.
- **Clear Form:** Click on `Clear Form` to clear the data from the form.
- **Viewing Ledger:** Click `Go to Ledger Page` to view transaction history.
- **Viewing Inventory:** Click `Go to Inventory Page` to view current inventory.

## Troubleshooting
### Database Connection Issues
- Ensure the `.env` file contains the correct `DB_URL`.
- Check if your PostgreSQL instance on Neon.tech is running.
- Use `pgAdmin` or `psql` to test the connection manually.

### GUI Not Displaying
- Ensure all dependencies are installed.
- Run `python main.py` in a terminal with the correct virtual environment activated.



