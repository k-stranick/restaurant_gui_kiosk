import csv  # used for reading and writing CSV files.
from colorama import Fore, init  # coloring terminal text output
init(autoreset=True)  # used to initialize colorama for terminal color output and automatically reset after use


def main():
    """
    primary function that loops through various menu options
    """
    menu = load_menu()
    print(f"\nRestaurant Menu Editor")
    while True:
        display_menu(menu)
        display_choice()
        choice = input("Choose Option (1-4): ")
        if choice == "1":
            add_item(menu)
        elif choice == "2":
            edit_item(menu)
        elif choice == "3":
            delete_item(menu)
        elif choice == "4":
            save_menu(menu)
            break
        else:
            print(Fore.RED + f"Invalid Choice Select Again")


def display_choice():
    """Displays menu options to the user."""
    print(f"\nOptions:")
    print(f"1. Add Item")
    print(f"2. Edit Item")
    print(f"3. Delete Item")
    print(f"4. Exit\n")


def display_menu(menu):
    """
    displays all items in the current menu with their assigned index number
    Parameters:
        menu (list): List of menu items.
    """
    print(f"\nMenu Items")
    for index_number, item in enumerate(menu):  # funtion to loop over the iterable menu and indexes them
        print(f"{index_number}. {item['Item ID']}, {item['Name']}: {item['Category']}: ${item['Price']}: {item['Description']}")


def response_prompt(prompt):
    """
        Query the user to decide whether to continue with the program.

    Parameters:
    - prompt (str): A string to display when requesting input from the user.

    Returns:
    - bool: True if the user enters 'Y', False if the user enters 'N'.

    The function continuously prompts the user until a valid input (Y/N) is provided,
    ensuring that the program only proceeds with a clear affirmative or negative from the user.
     Gets a yes/no response from the user based on the provided prompt

    """
    while True:
        response = input(prompt).upper()
        if response in ["Y", "N"]:
            return response == "Y"
        print(Fore.RED + f"\nInvalid input. Please enter Y or N.\n")


def load_menu():
    """
    Load the restaurant menu from 'menu_items.csv'.

    Returns:
        list: List of menu items. Returns an empty list if file not found.

    try block checks for the existence of menu.csv. If not the try/except block catches the filenotfounderror
    and creates the file if not
    the reader returns a reader object to iterate over lines and maps it to a dict
    """
    try:
        with open("menu_items.csv", "r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def save_menu(menu):
    """
    Save the menu to 'menu_items.csv'.

    Parameters:
        menu (list): List of menu items to be saved.
    this function opens the menu.csv and allows it to be overwritten. Create an object which operates like a regular
    writer but maps dictionaries onto output rows. In the writer variable the menu will be written into a dict with
    headers established by the column variable.
    """
    with open("menu_items.csv", "w", newline='') as file:
        columns = ["Item ID", "Name", "Category", "Price", "Description"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(menu)


def get_item_input():  # look up multiple return version 2
    """
    Prompt the user for menu item details.

    Returns:
        dict: Dictionary containing name, description, and price of the item.
              Returns None if user decides to exit input.
    this function allows the user to input menu items. Entered items will evaluate to true if entered correctly and
    stored in a dict for later use.
    """
    item_id = int(input(f"Enter item id (or 'exit' to stop): "))
    if item_id == "exit":
        return None
    name = input(f"\nEnter item name (or 'exit' to stop): ")
    if name.lower() == "exit":  # will evaluate to True if exit is entered in either upper or lowercase
        return None  # returns None value to be called later in add_item and edit_item
    description = input(f"Enter item description (or 'exit' to stop): ")[:50]
    if description.lower() == "exit":
        return None  # returns that
    category = input(f"Enter item category (or 'exit' to stop): ")
    if category.lower() == "exit":
        return None
    while True:  # loops until proper float is input
        price_input = input(f"Enter price (or 'exit' to stop): ")
        if price_input.lower() == "exit":
            return None
        try:  # this block converts strings into floats and returns ValueError if it cannot
            price = float(price_input)
            break
        except ValueError:
            print(Fore.RED + f"Invalid price. Please enter a valid decimal number or 'exit'.")
    return {'Item ID': item_id, 'Name': name, 'Category': category, 'Price': str(price), 'Description': description}


def save_changes(menu):
    """Prompt user to save changes and save if confirmed."""
    if response_prompt(f"Would you like to save changes?(y/n): "):
        print(Fore.RED + f"Changes Saved")
        save_menu(menu)


def add_item(menu):
    """
    Allow users to add items to the menu.

    Parameters:
        menu (list): List of current menu items.

    this looped function will append menu inputs to the menu and will use stored None to exit inputs it exit it typed
    only after items are added will the function prompt users to keep entering items or to save newly added items.
    if the user decides not to save then the program will break without saving.
    """
    while True:
        item = get_item_input()
        if item is None:
            print(f"Input Aborted.")
            break
        menu.append(item)

        if not response_prompt(f"\nWould you like to keep entering menu items?(y/n): "):
            save_changes(menu)
            break


def edit_item(menu):
    """
    Allow users to edit items in the menu.

    Parameters:
        menu (list): List of current menu items.
    this function allows the user to edit a selected index if the user selects an index outside the bounds
    an error is raised to gracefully catch this. If user enters none then the function is exited.
    """
    while True:  # figure out how to select each individual detail
        display_menu(menu)
        try:  # added ver 2 needed to catch valueerror
            index_number = int(input(f"Which item would you like to change?: "))
            if index_number < 0 or index_number >= len(menu):  # added to stop index error
                raise ValueError()
            item = get_item_input()
            if item is None:
                print(f"Edit Aborted")
                break

            menu[index_number] = item
            if not response_prompt(f"Would you like to keep editing menu items?(y/n): "):
                save_changes(menu)
                break
        except ValueError:
            print(Fore.RED + f"Invalid Entry Enter Valid Index")


def delete_item(menu):
    """
    Allow users to delete items from the menu.

    Parameters:
        menu (list): List of current menu items.
    """
    while True:
        display_menu(menu)
        index_input = (input(f"\nSelect item number to delete: "))

        if index_input.lower() == "exit":
            break
        try:
            index_number = int(index_input)
            if index_number < 0 or index_number >= len(menu):  # added to stop index error
                raise ValueError()
            item_name = menu[index_number]["Name"]
            if response_prompt(f"Are you sure you want to delete {item_name}?(y/n): "):
                del menu[index_number]
                print(Fore.YELLOW + f"{item_name} Deleted")
                save_changes(menu)
                break
        except ValueError:
            print(Fore.RED + f"Enter valid item number or 'exit'.")


if __name__ == "__main__":
    main()
