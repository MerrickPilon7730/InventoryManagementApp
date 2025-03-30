import tkinter as tk
from inventory_page import InventoryPage
from ledger_page import LedgerPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties 
        self.title("Inventory Management System")
        self.state("zoomed")

        # Create a container to hold the frames/views
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Initialize frames/views
        self.frames = {}
        for F in (InventoryPage, LedgerPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show inventory page on load
        self.show_frame(InventoryPage)

    # Function to navigate between frames/views
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
