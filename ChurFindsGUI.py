# Vince Vagay - 30036567
# Task 3

# This GUI was rapidly developed alongside Gemini 2.5 Flash and ChatGPT - GPT5

# I placed each widget on the screen.
# I manually did the alignments for the listbox.
# I manually did the Combobox, everything else was mainly me asking AI how to style something.

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QListWidget, QLabel, QMessageBox, 
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QListWidgetItem
)
from PyQt5.QtCore import Qt, QSize 
from PyQt5.QtGui import QIcon, QFont 
from PyQt5 import QtWidgets, uic

import processing

try:
    from Mongo import Mongo 
    from MarketPlace import MarketPlace
except ImportError:
    print("Warning: Mongo or MarketPlace modules not found.")
    class Mongo:
        def get_StoredListings(self):
            # Returns empty list as per user request to avoid dummy listings
            return []
# ----------------------------------------------------------------------------------

# These are global variables - Against best practices

# Options for the combobox of conditions
CONDITION_OPTIONS = [
        "New", 
        "Used", 
        "Used - Like New", 
        "Used - Good", 
        "For Parts/Not Working"
    ]

# Used for getting the index of a current listing
GLOBAL_SELECTED_INDEX = None

# Binds the cancel button to close the current window
def bind_cancel_button(window):
    if hasattr(window, "CancelButton"):
        window.CancelButton.clicked.connect(window.close)

# Responsible for my Edit Current Listing Window/GUI
class EditListingForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ChurFindsEdit.ui", self)  # Load your UI file
        self.CancelButton.clicked.connect(self.close)
        if hasattr(self, 'ConditionOptions'):
            # Populate the QComboBox
            self.ConditionOptions.addItems(CONDITION_OPTIONS)
            
            # Set the first option "New" as the default selection
            self.ConditionOptions.setCurrentIndex(0)
        self.EditListingButton.clicked.connect(self.process_and_edit_listing)
        self.mongo = Mongo()
        self.load_listing_data()

    # HAND CODED BY VINCE VAGAY
    def load_listing_data(self):
        
        # Testing to see if the current listing index was correctly passed
        index = GLOBAL_SELECTED_INDEX

        print(self.mongo.get_StoredListings()[index].ListingTitle)

        # A. Fill Text/Input Fields (using setPlainText for QPlainTextEdit)
        self.ListingNameInput.setPlainText(self.mongo.get_StoredListings()[index].ListingTitle)
        self.ListingDescInput.setPlainText(self.mongo.get_StoredListings()[index].Description)
        self.ListingPriceInput.setPlainText(f"{self.mongo.get_StoredListings()[index].ListingPrice:.2f}") # Format price to 2 decimal places
        self.ListingSNameInput.setPlainText(self.mongo.get_StoredListings()[index].SellerName)
        self.ListingSPhoneInput.setPlainText(self.mongo.get_StoredListings()[index].PhoneNum)
        self.ListingSEmailInput.setPlainText(self.mongo.get_StoredListings()[index].Email)

    def process_and_edit_listing(self):
        # It is the bridge between GUI widgets and the processing logic.
        # 1. PULL raw data from widgets
        name = self.ListingNameInput.toPlainText()
        condition = self.ConditionOptions.currentText()
        desc = self.ListingDescInput.toPlainText()
        price_str = self.ListingPriceInput.toPlainText()
        seller_name = self.ListingSNameInput.toPlainText()
        seller_phone = self.ListingSPhoneInput.toPlainText()
        seller_email = self.ListingSEmailInput.toPlainText()
        
        # Initialisting just in case
        price = None

        # 2. Validation & Conversion (GUI Responsibility)
        try:
            price = float(f"{float(price_str):.2f}")
        except ValueError:
            # Handle the error and display messages
            QtWidgets.QMessageBox.critical(self, "Input Error", "Please input a valid price")
            # 1. Clear the bad input from the widget
            self.ListingPriceInput.clear()
            # 2. Set focus back to the widget for easy re-entry
            self.ListingPriceInput.setFocus()
            # 3. Stop execution immediately
            return
        
        # For Testing
        # # Print price as initial input
        # print(name,condition,desc,price_str,seller_name,seller_phone,seller_email)
        # # Print price as converted
        # print(name,condition,desc,price,seller_name,seller_phone,seller_email)

        # Creates link to Mongo
        temp_mongo_instance = Mongo()
        # Temporary mongo instance
        temp_crud_processor = processing.CRUD(temp_mongo_instance)

        # Global Variable for current listing Index
        index = GLOBAL_SELECTED_INDEX

        # 3. Call the EditListing method on the new CRUD object, passing the parameters.
        EditListing = temp_crud_processor.EditListing(
            # Give it back it's original 6 Digit Unique Code
            listing_code = (self.mongo.get_StoredListings()[index].gen),
            name = name,
            condition = condition,
            price = price,        # Ensure this is the converted float price
            seller_name = seller_name,
            seller_phone = seller_phone,
            seller_email = seller_email,
            desc = desc,        # Description
            index = index,
            image_url = None # COMING FEATURE NO IMPLEMENTED
        )
    
        # 4. Handle the result and PUSH feedback to the GUI
        if EditListing:
            print(f"FAILURE: Could not add {name}.")
        else:
            print(f"Success {name} updated.")

class EditListingWindow(QMainWindow):
    def __init__(self):
        super(EditListingForm, self).__init__()
        
        # Load the .ui file
        ui_file = os.path.join(os.path.dirname(__file__), "ChurFindsEdit.ui")
        uic.loadUi(ui_file, self)

        self.setStyleSheet("""
            QMainWindow { background-color: #276F91; color: white; }
            QLabel#CompanyName { 
                font-size: 20pt; font-weight: bold; 
                qproperty-alignment: 'AlignHCenter'; 
                margin-bottom: 10px;
            }
            QListWidget { 
                 background-color: #385B75; color: white; 
                 border: 2px solid #1E5670; border-radius: 8px;
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
            }

            /* Specific style for Edit Listing Button */
            QPushButton#EditListingButton {
                background-color: #276F91;
                color: white; 
            }

            /* Default Hover State */
            QPushButton:hover { 
                background-color: #4edce4; 
            }

            /* Specific Hover State for Edit Listing Button */
            QPushButton#EditListingButton:hover {
                background-color: #385B75; 
                color: white;
            }
        """)

# Responsible for my Add New Listing Window/GUI
class AddListingForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ChurFindsAdd.ui", self)  # Load your UI file
        self.CancelButton.clicked.connect(self.close)
        if hasattr(self, 'ConditionOptions'):
            # Populate the QComboBox
            self.ConditionOptions.addItems(CONDITION_OPTIONS)
            
            # Set the first option "New" as the default selection
            self.ConditionOptions.setCurrentIndex(0)
        self.AddListingButton.clicked.connect(self.process_and_add_listing)

    def process_and_add_listing(self):
        # It is the bridge between GUI widgets and the processing logic.
        # 1. PULL raw data from widgets
        name = self.ListingNameInput.toPlainText()
        condition = self.ConditionOptions.currentText()
        desc = self.ListingDescInput.toPlainText()
        price_str = self.ListingPriceInput.toPlainText()
        seller_name = self.ListingSNameInput.toPlainText()
        seller_phone = self.ListingSPhoneInput.toPlainText()
        seller_email = self.ListingSEmailInput.toPlainText()
        
        # Initialisting just in case
        price = None

        # 2. Validation & Conversion (GUI Responsibility)
        try:
            price = float(f"{float(price_str):.2f}")
        except ValueError:
            # Handle the error and display messages
            QtWidgets.QMessageBox.critical(self, "Input Error", "Please input a valid price")
            # 1. Clear the bad input from the widget
            self.ListingPriceInput.clear()
            # 2. Set focus back to the widget for easy re-entry
            self.ListingPriceInput.setFocus()
            # 3. Stop execution immediately
            return
        
        # # For Testing
        # # Print price as initial input
        # print(name,condition,desc,price_str,seller_name,seller_phone,seller_email)
        # # Print price as converted
        # print(name,condition,desc,price,seller_name,seller_phone,seller_email)

        # Creates link to Mongo
        temp_mongo_instance = Mongo()
        # Temporary mongo instance
        temp_crud_processor = processing.CRUD(temp_mongo_instance)
        
        # 3. Call the AddListing method on the new CRUD object, passing the parameters.
        AddedListing = temp_crud_processor.AddListing(
            name = name,
            condition = condition,
            price = price,        # Ensure this is the converted float price
            seller_name = seller_name,
            seller_phone = seller_phone,
            seller_email = seller_email,
            desc = desc           # Description
        )
    
        # 4. Handle the result and PUSH feedback to the GUI
        if AddedListing:
            print(f"Success {name} added.")
        else:
            print(f"FAILURE: Could not add {name}.")

class AddListingWindow(QMainWindow):
    def __init__(self):
        super(AddListingForm, self).__init__()
        
        # Load the .ui file
        ui_file = os.path.join(os.path.dirname(__file__), "ChurFindsAdd.ui")
        uic.loadUi(ui_file, self)

        self.setStyleSheet("""
            QMainWindow { background-color: #276F91; color: white; }
            QLabel#CompanyName { 
                font-size: 20pt; font-weight: bold; 
                qproperty-alignment: 'AlignHCenter'; 
                margin-bottom: 10px;
            }
            QListWidget { 
                 background-color: #385B75; color: white; 
                 border: 2px solid #1E5670; border-radius: 8px;
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
            }

            /* Specific style for Edit Listing Button */
            QPushButton#EditListingButton {
                background-color: #276F91;
                color: white; 
            }

            /* Default Hover State */
            QPushButton:hover { 
                background-color: #4edce4; 
            }

            /* Specific Hover State for Edit Listing Button */
            QPushButton#EditListingButton:hover {
                background-color: #385B75; 
                color: white;
            }
            /* Specific Hover State for Edit Listing Button */
            QPushButton#EditListingButton:hover {
                background-color: #385B75; 
                color: white;
            }
        """)
        
# Everything below this line is purely AI coded, I only added \t to the listbox string formatting
# ----------------------------------------------------------------------------------


class MarketplaceTester(QMainWindow):
    # The following code before the __init__ was done in assistance from Google's Gemini and done by Vince
    def refresh_listings(self):
        # 1. Clear all existing items from the list widget
        self.listWidget.clear()
        
        # Reset the selection state and output label
        self.current_selected_code = None
        self.output_label.setText("Select an item to view details or edit/delete.")
        
        # 2. Get the updated list of listings from the database
        listings = self.crud_processor.GetListings()
        
        if not listings:
            QListWidgetItem("No listings found in the database.", self.listWidget)
            self.EditListingButton.setEnabled(False)
            self.DeleteListingButton.setEnabled(False)
            return

        # 3. Re-populate the list widget with the new data
        for listing in listings:
            item_text = listing.MarketListingInfo()
            item = QListWidgetItem(item_text, self.listWidget)
            # Store the unique 'gen' code in the item's UserRole for robust retrieval
            item.setData(Qt.UserRole, listing.gen)
            item.setFont(QFont("Arial", 10))
            
        # Refresh current listings and UI
        self.current_listings = self.all_listings[:]
        self.load_listings(self.current_listings)
        
    def delete_selected_listing(self):
        # Creates link to Mongo
        temp_mongo_instance = Mongo()
        # Temporary mongo instance
        temp_crud_processor = processing.CRUD(temp_mongo_instance)

        # Global Variable for current listing Index
        index = GLOBAL_SELECTED_INDEX

        # print(index)
        Delete = temp_crud_processor.DeleteListing(index)

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
            
    # Opens the Add New Listing Window
    def open_add_listing_form(self):
        self.add_listing_window = AddListingForm()

        # Center it over the main window
        parent_rect = self.geometry()
        form_rect = self.add_listing_window.frameGeometry()

        # Compute center point relative to the main window
        center_x = parent_rect.center().x() - form_rect.width() // 2
        center_y = parent_rect.center().y() - form_rect.height() // 2
        self.add_listing_window.move(center_x, center_y)

        # Show the window
        self.add_listing_window.show()
        self.add_listing_window.raise_()  # Bring it to front

    # Opens the Edit Current Listing Window
    def open_edit_listing_form(self):
        self.edit_listing_window = EditListingForm()

        # Center it over the main window
        parent_rect = self.geometry()
        form_rect = self.edit_listing_window.frameGeometry()

        # Compute center point relative to the main window
        center_x = parent_rect.center().x() - form_rect.width() // 2
        center_y = parent_rect.center().y() - form_rect.height() // 2
        self.edit_listing_window.move(center_x, center_y)

        # Show the window
        self.edit_listing_window.show()
        self.edit_listing_window.raise_()  # Bring it to front

    # Constructor
    def __init__(self):
        super().__init__()
        
        # Initialize internal state for filtering
        self.all_listings = []
        self.current_listings = []
        self.db_manager = None 
        self.add_listing_window = None # Keep a reference to prevent garbage collection
        
        ui_file_name = "ChurFindsUI.ui"

        # Initialize
        # 1. Create the Mongo object (which is still a local variable 'mongo')
        mongo = Mongo()
        
        # 2. Create the CRUD object, referencing it from the processing module
        #    AND store the results as instance variables (self.db_manager, self.crud_processor)
        self.db_manager = mongo
        self.crud_processor = processing.CRUD(self.db_manager)
        
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
            
            self.AddListingButton.clicked.connect(self.open_add_listing_form)
            
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
                    border: 2px solid #1E5670; border-radius: 8px;
                }
                QListWidget::item:selected {
                    background-color: #34C4C2; 
                    color: black;
                }
                QLabel#output_label {
                    color: white; padding: 10px; background-color: #1f3340; 
                    border-radius: 5px; min-height: 80px;
                }
                QPushButton {
                    min-height: 40px; 
                    min-width: 140px; 
                    padding: 8px 20px;
                    background-color: #34C4C2; color: #000000;
                    border: none; border-radius: 8px; font-weight: bold;
                }
                QPushButton#EditListingButton {
                    background-color: #276F91;
                    color: white;
                }
                QPushButton:hover { 
                    background-color: #4edce4; 
                }
                QPushButton#EditListingButton:hover {
                    background-color: #385B75;
                    color: white;
                }
            """)
            
            # CRITICAL for alignment: Set Monospaced Font
            from PyQt5.QtGui import QFont # Ensure QFont is accessible
            if self.listWidget:
                # Set font to monospaced for alignment
                new_font = QFont("Courier New", 7)
                self.listWidget.setFont(new_font) 
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
            # Note: The presence of Mongo is assumed by the user's initial code structure
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

            # Connect Button Signals (Implementation of user request to bind AddListingsButton)
            if self.AddListingsButton:
                self.AddListingsButton.clicked.connect(self.open_add_listing_form)
            if self.EditListingButton:
                self.EditListingButton.clicked.connect(self.open_edit_listing_form)
            if self.DeleteListingButton:
                self.DeleteListingButton.clicked.connect(self.delete_selected_listing)
        else:
            print("WARNING: 'listWidget' (QListWidget) not found after UI initialization. Check objectName.")

    # --- LISTING DISPLAY METHODS (UPDATED COLUMN ORDER) ---
    def load_listings(self, listings_to_load):
        # Populates the QListWidget with Item Title, Price.
        if not hasattr(self, 'listWidget') or self.listWidget is None:
            return 
        
        self.listWidget.clear()
        
        if not listings_to_load:
             self.listWidget.addItem("No listings found.")
             return
             
        # --- FIXED COLUMN WIDTHS ---
        LEFT_PADDING = " "
        MAX_ITEM_WIDTH = 25        # Total column width for Item Title
        MAX_ITEM_CONTENT_WIDTH = MAX_ITEM_WIDTH - len(LEFT_PADDING) 
        
        MAX_DESC_WIDTH = 50
        
        CONDITION_WIDTH = 15
        PRICE_WIDTH = 8             
        
        # Define the separator string (3 characters)
        SEPARATOR = "  " 
        
        # --- Add Header Row (Item Title | Price | Condition | Description) ---
        
        # 1. Item Title Header (Left padded)
        header_content_title = f"{'Item Title\t\t\t':<{MAX_ITEM_CONTENT_WIDTH}}"
        header_item = LEFT_PADDING + header_content_title
        
        # 2. Price Header (Right aligned)
        header_price = f"{'Price':>{PRICE_WIDTH}}"
        
        # # 3. Condition Header (Left aligned)
        header_cond = f"\t{'Condition':<{CONDITION_WIDTH}}"
        
        # # 4. Description Header (Left aligned)
        # header_desc = f"{'Description':<{MAX_DESC_WIDTH}}"
        
        # Construct the header text in the new order: Title | Price | Condition | Description
        header_text = (
            f"{header_item}"
            f"{SEPARATOR}{header_price}"
            f"\t{SEPARATOR}{header_cond}"
            # f"{SEPARATOR}{header_desc}"
        )
        
        # Add Header Row and make it non-selectable
        header_item_widget = QListWidgetItem(header_text)
        # Disable selection and make the item unfocusable/uneditable
        header_item_widget.setFlags(Qt.NoItemFlags) 
        self.listWidget.addItem(header_item_widget)

        # Add a separator line (also non-selectable)
        separator_item_widget = QListWidgetItem("_" * 85)
        # Disable selection and make the item unfocusable/uneditable
        separator_item_widget.setFlags(Qt.NoItemFlags) 
        self.listWidget.addItem(separator_item_widget)

        for listing_obj in listings_to_load:
            # Ensure methods exist on the listing object before calling
            if not hasattr(listing_obj, 'GetListingTitle'):
                 print("Error: Listing object is missing required methods. Skipping.")
                 continue

            title = f"{listing_obj.GetListingTitle()}\t\t"
            # full_description = listing_obj.GetDescription() 
            price_text = f"\t$ {listing_obj.GetListingPrice():.2f}  "
            condition_text = f"\t{listing_obj.GetCondition()}"
            
            # --- 1. Format Item (Title) ---
            display_title = title
            # Truncate title content if it exceeds the calculated width
            if len(title) > MAX_ITEM_CONTENT_WIDTH - 3: 
                display_title = title[:MAX_ITEM_CONTENT_WIDTH - 3] + "..."
            
            # Left-align the title content and prepend the padding
            title_content_part = f"{display_title:<{MAX_ITEM_CONTENT_WIDTH}}"
            item_part = LEFT_PADDING + title_content_part
            
            # --- 2. Format Price (Right aligned) ---
            price_part = f"\t{price_text:>{PRICE_WIDTH}}"
            
            # # --- 3. Format Condition (Left aligned) ---
            condition_part = f"{condition_text:<{CONDITION_WIDTH}}"
            
            # # --- 4. Format Short Description (Left aligned) ---
            # short_description = full_description
            # if len(full_description) > MAX_DESC_WIDTH - 3:
            #     short_description = full_description[:MAX_DESC_WIDTH - 3] + "..."
            # desc_part = f"{short_description:<{MAX_DESC_WIDTH}}"
            
            # 5. Construct the final line in the new order: Title | Price | Condition | Description
            formatted_item = (
                f"{item_part}"
                f"{SEPARATOR}{price_part}"      # Price is second
                f"{SEPARATOR}{condition_part}"
                # f"{SEPARATOR}{desc_part}"        # Description is last
            )
            
            self.listWidget.addItem(formatted_item)

    # For each time the user clicks on the listbox
    def handle_listing_click(self, row_index):
        # Called when a list item is clicked.
        
        # Adjust index because we added a header (index 0) and separator line (index 1)
        data_index = row_index - 2 

        if data_index >= 0 and data_index < len(self.current_listings):
            clicked_listing_obj = self.current_listings[data_index]
            
            # Detailed display content (This is the full description)
            details = f"Title: {clicked_listing_obj.GetListingTitle()}\n"
            details += f"Price: ${clicked_listing_obj.GetListingPrice():.2f}\n"
            
            if hasattr(self, 'output_label') and self.output_label is not None:
                self.output_label.setText(details)
            print(f"Selected Listing: {clicked_listing_obj.GetListingTitle()}")
        else:
            if hasattr(self, 'output_label') and self.output_label is not None:
                self.output_label.setText("Select a listing above to see details.")
            print("Selection cleared or invalid.")
        
        # Adjust index because we added a header (index 0) and separator line (index 1)
        data_index = row_index - 2 

        if data_index >= 0 and data_index < len(self.current_listings):
            clicked_listing_obj = self.current_listings[data_index]
            
            # --- CRITICAL CHANGE: Store the index, not the unique code ---
            self.selected_listing_index = data_index 

            # --- OUTPUT: Only prints the index (as requested) ---
            print(f"Selected Listing Index (in current_listings): {self.selected_listing_index}")

            global GLOBAL_SELECTED_INDEX
            GLOBAL_SELECTED_INDEX = int(self.selected_listing_index)
            
            # Update the output label for visual confirmation (optional)
            if hasattr(self, 'output_label') and self.output_label is not None:
                self.output_label.setText(f"Listing at index {self.selected_listing_index} selected. Click 'Edit Listing' to modify.")

    # --- Fallback UI for testing without the .ui file (PURE LAYOUT) ---
    def setup_fallback_ui(self):
        # Sets up the UI if the .ui file is not found.
        # Includes buttons and uses layouts for responsiveness.

        # 1. Initialize Elements using REQUIRED NAMES
        self.listWidget = QListWidget(objectName='listWidget') 
        self.output_label = QLabel("Select a listing above to see details.", objectName='output_label')
        self.CompanyName = QLabel("Chur Finds Marketplace", objectName='CompanyName') 
        self.AddListingsButton = QPushButton("Add Listing", objectName='AddListingsButton')
        self.EditListingButton = QPushButton("Edit Listing", objectName='EditListingButton')
        self.DeleteListingButton = QPushButton("Delete Listing", objectName='DeleteListingButton')
        self.RefreshButton = QPushButton("Refresh Listings", objectName='RefreshButton')
        
        self.setWindowTitle("Chur Finds Marketplace - Fallback UI")
        # Window size remains at 1400px wide
        self.setMinimumSize(QSize(1000, 750)) 

        # CRITICAL for alignment: Set Monospaced Font
        from PyQt5.QtGui import QFont 
        # Set font to monospaced for alignment
        new_font = QFont("Courier New", 7)
        self.listWidget.setFont(new_font)
        print(f"DEBUG: Fallback UI: Attempted to set list font size to {new_font.pointSize()}pt.")


        # 2. Main Container and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Apply the global stylesheet defined in __init__ for background and color
        self.setStyleSheet("""
            QMainWindow { background-color: #276F91; color: white; }
            QLabel#CompanyName { 
                font-size: 20pt; font-weight: bold; 
                qproperty-alignment: 'AlignHCenter'; 
                margin-bottom: 10px;
            }
            QListWidget { 
                 background-color: #385B75; color: white; 
                 border: 2px solid #1E5670; border-radius: 8px;
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
            }
            
            /* Specific style for Edit Listing Button (RETAINED) */
            QPushButton#EditListingButton {
                background-color: #276F91;
                color: white; 
            }
            
            /* Default Hover State */
            QPushButton:hover { 
                background-color: #4edce4; 
            }
            
            /* Specific Hover State for Edit Listing Button */
            QPushButton#EditListingButton:hover {
                background-color: #385B75; 
                color: white;
            }
        """)

        main_layout = QVBoxLayout(central_widget)
        
        # 3. Title (CompanyName) 
        self.CompanyName.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.CompanyName)
        
        # 4. Buttons Layout (Horizontal for Add, Edit, Delete)
        button_layout = QHBoxLayout()
        
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
        main_layout.addWidget(self.listWidget)
        
        # 7. Output Label 
        main_layout.addWidget(self.output_label)
        
        # 8. Connect signals for fallback UI
        self.listWidget.currentRowChanged.connect(self.handle_listing_click)
        
        # Connect the Add Listing button to the new method
        self.AddListingsButton.clicked.connect(self.open_add_listing_form)

        # Connect the Edit Listing button to the new method
        self.EditListingButton.clicked.connect(self.open_edit_listing_form)

        # Connect the Add Listing button to the new method
        self.DeleteListingButton.clicked.connect(processing.DeleteListing(GLOBAL_SELECTED_INDEX))

        #
        self.RefreshButton.click.connect(self.refresh_listings)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    # This message will only appear if the imports failed
    if 'Mongo' in globals() and 'MarketPlace' in globals() and not hasattr(MarketPlace, 'GetListingTitle'):
        print("Mongo failed to import.")
    window = MarketplaceTester()
    
    # 3. Show the main window
    window.show()
    
    # 4. Start the application's event loop
    sys.exit(app.exec_())
