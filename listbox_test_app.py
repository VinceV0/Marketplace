import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QLabel, QMessageBox, 
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize 
from PyQt5.QtGui import QIcon, QFont 
from PyQt5 import uic 

# --- DATA IMPORTS ---
from Mongo import Mongo 
from MarketPlace import MarketPlace
# --------------------

class MarketplaceTester(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize internal state for filtering
        self.all_listings = []
        self.current_listings = []
        self.db_manager = None 
        
        ui_file_name = "ChurFindsUI.ui"
        
        # --- 1. Load the UI file created in Qt Designer ---
        try:
            print(f"Attempting to load UI file: {os.path.abspath(ui_file_name)}")
            uic.loadUi(ui_file_name, self)
            print("UI file loaded successfully.")

            # Set a minimum size for the main window to ensure layout stretching (important for the listbox width)
            # Window size remains at 1400px wide
            self.setMinimumSize(QSize(1400, 750)) 

            # Retrieve widget references 
            self.listWidget = getattr(self, 'listWidget', None)
            self.output_label = getattr(self, 'output_label', None)
            self.CompanyName = getattr(self, 'CompanyName', None)
            
            # Retrieve Button references 
            self.AddListingsButton = getattr(self, 'AddListingsButton', None)
            self.EditListingButton = getattr(self, 'EditListingButton', None)
            self.DeleteListingButton = getattr(self, 'DeleteListingButton', None)
            
            # Applying styling globally (buttons, list widget, background)
            self.setStyleSheet("""
                QMainWindow { background-color: #276F91; color: white; }
                QLabel#CompanyName { 
                    font-size: 20pt; font-weight: bold; 
                    qproperty-alignment: 'AlignHCenter'; 
                    margin-bottom: 10px;
                }
                QListWidget { 
                     background-color: #385B75; color: white; 
                     /* Border color changed to #1E5670 */
                     border: 2px solid #1E5670; border-radius: 8px;
                     /* Removed fixed font size to allow QFont to control it */
                }
                QListWidget::item:selected {
                    background-color: #34C4C2; 
                    color: black;
                }
                QLabel#output_label {
                    color: white; padding: 10px; background-color: #1f3340; 
                    border-radius: 5px; min-height: 80px;
                }
                
                /* Default Button Style */
                QPushButton {
                    min-height: 40px; 
                    min-width: 140px; 
                    padding: 8px 20px;
                    background-color: #34C4C2; color: #000000;
                    border: none; border-radius: 8px; font-weight: bold;
                    transition: background-color 0.2s; 
                }
                
                /* Specific style for Edit Listing Button (RETAINED) */
                QPushButton#EditListingButton {
                    background-color: #276F91;
                    color: white; /* Ensure text is visible on dark background */
                }
                
                /* Default Hover State */
                QPushButton:hover { 
                    background-color: #4edce4; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                
                /* Specific Hover State for Edit Listing Button */
                QPushButton#EditListingButton:hover {
                    background-color: #385B75; /* Slightly lighter shade for hover effect */
                    color: white;
                }
            """)
            
            # CRITICAL for alignment: Set Monospaced Font
            from PyQt5.QtGui import QFont # Ensure QFont is accessible
            if self.listWidget:
                # REVERTED: Set back to the user-requested size of 7pt
                new_font = QFont("Courier New", 7)
                self.listWidget.setFont(new_font) 
                # Print the size for debugging purposes
                print(f"DEBUG: Attempted to set list font size to {new_font.pointSize()}pt.")

        except FileNotFoundError:
            print(f"Error: '{ui_file_name}' not found at current path. Falling back to code-based UI with stable layout.")
            self.setup_fallback_ui() # Call the fallback method
            
        
        # --- Setting the Application Icon ---
        try:
            self.setWindowIcon(QIcon('chur_finds_logo.png')) 
        except Exception:
            print("Warning: chur_finds_logo.png not found. Using default icon.")

        # --- 2. Data Initialization (Synchronous Load) ---
        print("Initializing Mongo connection and loading data synchronously...")
        try:
            self.db_manager = Mongo()
            # Fetch data right at startup
            self.all_listings = self.db_manager.get_StoredListings() 
            self.current_listings = self.all_listings[:] 
            print(f"Successfully loaded {len(self.all_listings)} listings from database.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect or load data: {e}")
            self.all_listings = []
            self.current_listings = []
            print(f"Error: Database connection failed. {e}")


        # --- 3. Connect Signals and Load List ---
        if hasattr(self, 'listWidget') and self.listWidget is not None:
            self.load_listings(self.current_listings)
            # Connect the click signal
            self.listWidget.currentRowChanged.connect(self.handle_listing_click)

            # Connect Button Signals 
            if self.AddListingsButton:
                self.AddListingsButton.clicked.connect(self.show_add_listing_dialog)
            if self.EditListingButton:
                self.EditListingButton.clicked.connect(lambda: self.show_feature_pending("Edit Listing"))
            if self.DeleteListingButton:
                self.DeleteListingButton.clicked.connect(self.delete_selected_listing)

        else:
            print("WARNING: 'listWidget' (QListWidget) not found after UI initialization. Check objectName.")

    # --- Placeholder Functions ---
    def show_add_listing_dialog(self):
        """Placeholder for launching the Add Listing Dialog."""
        QMessageBox.information(self, "Feature Pending", "We are about to build the 'Add Listing' window!")

    def show_feature_pending(self, feature_name):
        """Generic handler for features not yet implemented."""
        QMessageBox.information(self, "Feature Pending", f"The '{feature_name}' feature is coming soon!")

    # --- DELETE LOGIC ---
    def delete_selected_listing(self):
        """
        Handles the selection and confirmation of deleting a listing.
        """
        if not self.listWidget or not self.db_manager:
            QMessageBox.warning(self, "Setup Error", "Database manager or List Widget not initialized.")
            return

        selected_row = self.listWidget.currentRow()

        # Adjust index because we added a header and separator line
        data_index = selected_row - 2 

        if data_index < 0 or data_index >= len(self.current_listings):
            # Check if user selected the header or separator, or nothing
            if selected_row > 1: # Only show warning if a data row wasn't clicked
                 QMessageBox.warning(self, "Selection Required", "Please select a valid listing to delete first.")
            return

        # Get the listing object to confirm with the user
        listing_to_delete = self.current_listings[data_index]
        title = listing_to_delete.GetListingTitle()

        # Confirmation Dialog
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion',
            f"Are you sure you want to delete the listing: \n'{title}'?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print(f"User confirmed deletion of: {title}. (Database deletion logic pending)")
            
            # Find and delete the item from the master list
            try:
                self.all_listings.pop(self.all_listings.index(listing_to_delete))
            except ValueError:
                pass # Already deleted or not found
            
            # Refresh current listings and UI
            self.current_listings = self.all_listings[:]
            self.load_listings(self.current_listings)
            
            # Clear details output
            if self.output_label:
                self.output_label.setText(f"Listing '{title}' successfully deleted (locally simulated).")
        else:
            print(f"Deletion cancelled for: {title}")


    # --- LISTING DISPLAY METHODS (REVERTED COLUMN WIDTHS) ---
    def load_listings(self, listings_to_load):
        """
        Populates the QListWidget with Item, Short Description, Condition, and Price, 
        using string padding for guaranteed alignment and clearer visual division.
        """
        if not hasattr(self, 'listWidget') or self.listWidget is None:
            return 
        
        self.listWidget.clear()
        
        if not listings_to_load:
             self.listWidget.addItem("No listings found.")
             return
             
        # --- FIXED COLUMN WIDTHS (REVERTED) ---
        LEFT_PADDING = " " * 5      # 5 spaces for left padding
        MAX_ITEM_WIDTH = 40         # Total column width
        MAX_ITEM_CONTENT_WIDTH = MAX_ITEM_WIDTH - len(LEFT_PADDING) # 35 characters for title content
        
        MAX_DESC_WIDTH = 60   
        
        CONDITION_WIDTH = 11
        PRICE_WIDTH = 8             # Reverted to 8
        
        # Define the separator string (7 characters)
        SEPARATOR = "   |   " 
        
        # --- Add Header Row (Item | Description | Condition | Price) ---
        # Item Header (Left padded)
        header_content = f"{'Item':<{MAX_ITEM_CONTENT_WIDTH}}"
        header_item = LEFT_PADDING + header_content
        
        # Other Headers (Left aligned)
        header_desc = f"{'Description':<{MAX_DESC_WIDTH}}"
        header_cond = f"{'Condition':<{CONDITION_WIDTH}}"
        
        # Price Header (Right aligned)
        header_price = f"{'Price':>{PRICE_WIDTH}}"
        
        # NOTE: Item column is exactly 40 characters wide and immediately followed by the separator.
        header_text = (
            f"{header_item}"
            f"{SEPARATOR}{header_desc}"
            f"{SEPARATOR}{header_cond}"
            f"{SEPARATOR}{header_price}"
        )
        
        # Add a placeholder for the header that can't be selected
        self.listWidget.addItem(header_text)
        
        # Add a separator line
        self.listWidget.addItem("-" * len(header_text))

        for listing_obj in listings_to_load:
            title = listing_obj.GetListingTitle()
            full_description = listing_obj.GetDescription() 
            price_text = f"${listing_obj.GetListingPrice():.2f}"
            condition_text = listing_obj.GetCondition()
            
            # --- 1. Format Item (Title) ---
            
            display_title = title
            # Truncate title content if it exceeds the 35 character width
            if len(title) > MAX_ITEM_CONTENT_WIDTH - 3: 
                display_title = title[:MAX_ITEM_CONTENT_WIDTH - 3] + "..."
            
            # Left-align the title content (35 chars) and prepend the 5 char padding
            title_content_part = f"{display_title:<{MAX_ITEM_CONTENT_WIDTH}}"
            item_part = LEFT_PADDING + title_content_part
            
            # --- 2. Format Short Description (60 CHARS WIDE) ---
            short_description = full_description
            if len(full_description) > MAX_DESC_WIDTH - 3:
                short_description = full_description[:MAX_DESC_WIDTH - 3] + "..."
            desc_part = f"{short_description:<{MAX_DESC_WIDTH}}"
            
            # --- 3. Format Condition and Price ---
            condition_part = f"{condition_text:<{CONDITION_WIDTH}}"
            
            # Price part (Right aligned - 8 chars wide)
            price_part = f"{price_text:>{PRICE_WIDTH}}"
            
            # 4. Construct the final line 
            formatted_item = (
                f"{item_part}"
                f"{SEPARATOR}{desc_part}"
                f"{SEPARATOR}{condition_part}"
                f"{SEPARATOR}{price_part}"       
            )
            
            self.listWidget.addItem(formatted_item)
            

    def handle_listing_click(self, row_index):
        """Called when a list item is clicked."""
        
        # Adjust index because we added a header (index 0) and separator line (index 1)
        data_index = row_index - 2 

        if data_index >= 0 and data_index < len(self.current_listings):
            clicked_listing_obj = self.current_listings[data_index]
            
            # Detailed display content (This is the full description)
            details = f"Title: {clicked_listing_obj.GetListingTitle()}\n"
            details += f"Price: ${clicked_listing_obj.GetListingPrice():.2f}\n"
            details += f"Condition: {clicked_listing_obj.GetCondition()}\n"
            details += f"Seller: {clicked_listing_obj.GetSellerName()}\n\n"
            details += f"Description: {clicked_listing_obj.GetDescription()}"
            
            if hasattr(self, 'output_label') and self.output_label is not None:
                self.output_label.setText(details)
            print(f"Selected Listing: {clicked_listing_obj.GetListingTitle()}")
        else:
            if hasattr(self, 'output_label') and self.output_label is not None:
                self.output_label.setText("Select a listing above to see details.")
            print("Selection cleared or invalid.")


    # --- Fallback UI for testing without the .ui file (PURE LAYOUT) ---
    def setup_fallback_ui(self):
        """
        Sets up the UI if the .ui file is not found.
        Includes buttons and uses layouts for responsiveness.
        """
        
        # 1. Initialize Elements using REQUIRED NAMES
        self.listWidget = QListWidget(objectName='listWidget') 
        self.output_label = QLabel("Select a listing above to see details.", objectName='output_label')
        self.CompanyName = QLabel("Chur Finds Marketplace", objectName='CompanyName') 
        self.AddListingsButton = QPushButton("Add Listing", objectName='AddListingsButton')
        self.EditListingButton = QPushButton("Edit Listing", objectName='EditListingButton')
        self.DeleteListingButton = QPushButton("Delete Listing", objectName='DeleteListingButton')
        
        self.setWindowTitle("Chur Finds Marketplace - Fallback UI")
        # Window size remains at 1400px wide
        self.setMinimumSize(QSize(1400, 750)) 

        # CRITICAL for alignment: Set Monospaced Font
        from PyQt5.QtGui import QFont 
        # REVERTED: Set back to the user-requested size of 7pt
        new_font = QFont("Courier New", 7)
        self.listWidget.setFont(new_font)
        print(f"DEBUG: Fallback UI: Attempted to set list font size to {new_font.pointSize()}pt.")


        # 2. Main Container and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #276F91; color: white;") 
        
        main_layout = QVBoxLayout(central_widget)
        
        # 3. Title (CompanyName) 
        self.CompanyName.setAlignment(Qt.AlignCenter)
        self.CompanyName.setStyleSheet("font-size: 20pt; font-weight: bold; margin-bottom: 10px; color: white;")
        main_layout.addWidget(self.CompanyName)
        
        # 4. Buttons Layout (Horizontal for Add, Edit, Delete)
        button_layout = QHBoxLayout()
        
        # Default style for buttons (Add and Delete)
        default_button_style = """
            min-height: 40px; 
            min-width: 140px; 
            padding: 8px 20px;
            background-color: #34C4C2; color: #000000;
            border: none; border-radius: 8px; font-weight: bold;
        """
        
        # Specific style for Edit button (RETAINED)
        edit_button_style = """
            min-height: 40px; 
            min-width: 140px; 
            padding: 8px 20px;
            background-color: #276F91; color: white;
            border: none; border-radius: 8px; font-weight: bold;
        """
        
        self.AddListingsButton.setStyleSheet(default_button_style)
        self.EditListingButton.setStyleSheet(edit_button_style)
        self.DeleteListingButton.setStyleSheet(default_button_style)
        
        button_layout.addStretch(1) 
        button_layout.addWidget(self.AddListingsButton)
        button_layout.addWidget(self.EditListingButton)
        button_layout.addWidget(self.DeleteListingButton)
        button_layout.addStretch(1) 
        main_layout.addLayout(button_layout) 

        # 5. Listings Header
        listings_header = QLabel("--- Available Listings ---")
        listings_header.setAlignment(Qt.AlignCenter)
        listings_header.setStyleSheet("color: #34C4C2; font-size: 16pt; margin-top: 10px; margin-bottom: 5px;")
        main_layout.addWidget(listings_header)

        # 6. List Widget 
        self.listWidget.setStyleSheet("background-color: #385B75; color: white; border: 2px solid #1E5670;")
        main_layout.addWidget(self.listWidget)
        
        # 7. Output Label 
        self.output_label.setStyleSheet("color: white; padding: 10px; background-color: #1f3340; border-radius: 5px; min-height: 80px;")
        main_layout.addWidget(self.output_label)
        
        # 8. Connect signals for fallback UI
        self.listWidget.currentRowChanged.connect(self.handle_listing_click)
        self.AddListingsButton.clicked.connect(self.show_add_listing_dialog)
        self.EditListingButton.clicked.connect(lambda: self.show_feature_pending("Edit Listing"))
        self.DeleteListingButton.clicked.connect(self.delete_selected_listing)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    window = MarketplaceTester()
    window.show()
    sys.exit(app.exec_())
