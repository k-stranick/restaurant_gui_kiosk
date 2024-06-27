import csv
import guizero as gz
from menu_item import MenuItem


# Standalone function for loading menu items
def load_menu_items_from_csv(csv_file):
    menu = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                item_id, name, category, price, description = row
                category = category.upper()
                if category not in menu:
                    menu[category] = []
                menu[category].append(MenuItem(int(item_id), name, category, float(price), description))
    except FileNotFoundError:
        gz.error("File Error", "CSV file not found.")
        return None
    return menu
