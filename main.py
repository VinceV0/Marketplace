import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class MarketplaceTester(QMainWindow):
    def __init__(self):
        super().__init__()
        # Updated window title here
        self.setWindowTitle("Chur Finds Marketplace")
        self.setGeometry(100, 100, 600, 500)
        
        # --- 1. Simulate Marketplace Data (Your mongo.storedListings equivalent) ---
        self.listings_data = [
            {'id': 101, 'title': 'Vintage Kiwi Rugby Jersey', 'price': 50.00},
            {'id': 102, 'title': 'Handmade Bee-Themed Soap', 'price': 8.50},
            {'id': 103, 'title': 'Used Mountain Bike - Size L', 'price': 450.00},
            {'id': 104, 'title': 'Bag of Local Apples (Organic)', 'price': 5.00},
            {'id': 105, 'title': 'Childrens Books Bundle', 'price': 15.00},
        ]

        self.setup_ui()
        self.load_listings()

    def setup_ui(self):
        """Sets up the central widget, layout, and QListWidget."""
        
        # Create a central widget (required for QMainWindow)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create a vertical layout to stack widgets
        layout = QVBoxLayout(central_widget)

        # Title Label
        title_label = QLabel("Click an Item Below to See Details:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; color: #34C4C2;")
        layout.addWidget(title_label)

        # --- 2. Create the QListWidget (The Listbox) ---
        self.listing_list_widget = QListWidget()
        self.listing_list_widget.setStyleSheet("font-size: 14pt;")
        layout.addWidget(self.listing_list_widget)

        # Output Label to show results of the click
        self.output_label = QLabel("Selection details will appear here...")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("color: white; padding: 10px; background-color: #2D485C; border-radius: 5px;")
        layout.addWidget(self.output_label)

        # --- 3. Attach the Python Code (Connect the signal) ---
        # The 'currentRowChanged' signal fires when the selected item index changes.
        self.listing_list_widget.currentRowChanged.connect(self.handle_listing_click)


    def load_listings(self):
        """Populates the QListWidget with data from self.listings_data."""
        
        # Clear the list before reloading (good practice)
        self.listing_list_widget.clear()
        
        for listing in self.listings_data:
            # We only show the 'title' in the listbox
            self.listing_list_widget.addItem(listing['title'])


    # --- 4. The Function that Triggers on Click ---
    def handle_listing_click(self, row_index):
        """
        Called when a list item is clicked. 
        'row_index' is the zero-based index of the clicked item.
        """
        
        # Ensure a valid index was clicked (it shouldn't be -1 if triggered by a click)
        if row_index >= 0 and row_index < len(self.listings_data):
            
            # Retrieve the full data object using the index
            clicked_listing = self.listings_data[row_index]
            
            # --- Test and Display the Result ---
            output_text = (
                f"INDEX SELECTED: {row_index}\n"
                f"TITLE: {clicked_listing['title']}\n"
                f"PRICE: ${clicked_listing['price']:.2f}\n"
                f"Action: Preparing to show details for ID {clicked_listing['id']}"
            )
            
            # Update the output label
            self.output_label.setText(output_text)
            print(f"Clicked Listing Data: {clicked_listing}")
            
        else:
            self.output_label.setText("Error: Invalid selection.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarketplaceTester()
    window.show()
    sys.exit(app.exec_())
