from gui_app import GUIApp
from utilities import load_menu_items_from_csv

# Main script
menu_data = load_menu_items_from_csv("menu_items.csv")
if menu_data:
    gui_app = GUIApp("Fūdo Fusion Menu", menu_data)
    gui_app.display()
else:
    print("Failed to load the menu items.")