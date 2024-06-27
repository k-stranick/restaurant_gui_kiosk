import guizero as gz
from order import Order


class GUIApp:
    def __init__(self, app_title, menu_data_param):
        self.app = gz.App(title=app_title, width=700, height=800)
        self.menu_data = menu_data_param
        self.order = Order()
        self.category_combo = None
        self.item_list = None
        self.description_box = None
        self.quantity_box = None
        self.order_summary_box = None
        self.create_widgets()
        self.app.tk.resizable(False, False)  # lock to full screen

    def update_order_summary_box(self):
        summary = self.order.get_summary()
        self.order_summary_box.value = summary  # Update the text in the order summary box

    def create_box(self, layout='grid', align='top', border=False):
        """Create a guizero Box with specified layout, alignment, and optional border."""
        box = gz.Box(self.app, layout=layout, align=align)
        if border:
            box.border = True
        return box

    def create_welcome(self):
        # Welcome text at top
        welcome_box = self.create_box(border=True)
        gz.Text(welcome_box, text="Welcome to Fūdo Fusion", grid=[0, 0, 2, 1], size=20, font="Arial")
        gz.Text(welcome_box, text="Select a category, choose an item, and enter the quantity.", grid=[0, 1, 2, 1],
                size=12, font="Arial")

    def create_category_selection(self):
        # Category combo box NEED TO ADD BLANK FOR FIRST SELECTION
        category_box = self.create_box()
        gz.Text(category_box, text="Categories:", grid=[0, 0])
        combo_options = ["SELECT A CATEGORY"] + list(self.menu_data.keys())
        self.category_combo = gz.Combo(category_box, options=combo_options, command=self.update_items_list,
                                       grid=[1, 0])

    def create_item_list(self):
        # Item list box
        item_list_box = gz.Box(self.app, layout="grid", align="top")
        self.item_list = gz.ListBox(item_list_box, command=self.item_selected, grid=[0, 0], align="top", width=240,
                                    height=250)

    def create_description_box(self):
        # Description box
        description_box = self.create_box()
        gz.Text(description_box, text="Description:", grid=[0, 0])
        self.description_box = gz.TextBox(description_box, multiline=True, scrollbar=True, grid=[0, 1], align="top",
                                          width=50, height=5)
        self.description_box.disable()

    def create_action_buttons(self):
        # Box for action buttons
        action_box = self.create_box()
        gz.Text(action_box, text="Quantity:", grid=[0, 0])
        self.quantity_box = gz.TextBox(action_box, grid=[1, 0])
        gz.PushButton(action_box, text="Add to Order", command=self.add_to_order, grid=[2, 0])
        gz.PushButton(action_box, text="Remove Item", command=self.remove_item, grid=[3, 0])

    def create_order_summary_box(self):
        # Order Summary box
        order_summary_box = self.create_box()
        gz.Text(order_summary_box, text="Order Summary:", grid=[0, 0])
        self.order_summary_box = gz.TextBox(order_summary_box, multiline=True, scrollbar=True, grid=[0, 1],
                                            width=50, height=10)

    def create_check_out(self):
        # Check out box and button
        check_out_box = self.create_box()
        gz.PushButton(check_out_box, text="Check Out", command=self.check_out, grid=[0, 0])

    def create_widgets(self):
        self.create_welcome()
        self.create_category_selection()
        self.create_item_list()
        self.create_description_box()
        self.create_action_buttons()
        self.create_order_summary_box()
        self.update_order_summary_box()
        self.create_check_out()

    def update_items_list(self):
        selected_category = self.category_combo.value
        if selected_category == "SELECT A CATEGORY":  # Check if the selection is an empty string
            self.item_list.clear()  # Clear the item list
        else:
            # Continue with the normal behavior when a valid category is selected
            self.item_list.clear()
            for item in self.menu_data[selected_category]:
                item_display = f"{item.name} | ${item.price:.2f}"  # Format to show name and price
                self.item_list.append(item_display)

    def item_selected(self):
        selected_item_display = self.item_list.value
        # Handle the case where no item is selected, perhaps by clearing the description box or displaying a message
        if not selected_item_display:
            self.description_box.value = ""
            return

        selected_item_name = selected_item_display.split(' | ')[0]  # Extract the name part
        for category, items in self.menu_data.items():
            for item in items:
                if item.name == selected_item_name:
                    self.description_box.value = item.description
                    break

    def add_to_order(self):
        selected_item_display = self.item_list.value
        if not selected_item_display:
            gz.error("Selection Error", "Please select a category and/or an item.")
            return
        selected_item_name = selected_item_display.split(' | ')[0]
        try:
            quantity = int(self.quantity_box.value)
            if quantity <= 0:
                raise ValueError
            for category, items in self.menu_data.items():
                for item in items:
                    if item.name == selected_item_name:
                        self.order.add_item(item, quantity)
                        self.update_order_summary_box()
                        self.quantity_box.value = ""
                        return
        except ValueError:
            gz.error("Input Error", "Please enter a valid quantity.")

    def remove_item(self):
        selected_item_display = self.item_list.value
        if not selected_item_display:
            gz.error("Selection Error", "Please select an item and enter amount to remove.")
            return
        selected_item_name = selected_item_display.split(' | ')[0]

        try:
            quantity = int(self.quantity_box.value)
            if quantity <= 0:
                raise ValueError

            # Check if the item is in the order and if the quantity to remove is appropriate
            for menu_item in self.order.items:
                if menu_item.name == selected_item_name:
                    if self.order.items[menu_item] >= quantity:
                        self.order.remove_item(menu_item, quantity)  # Use the method in Order class
                        self.update_order_summary_box()
                        self.quantity_box.value = ""
                        gz.info("Item Removed", f"Removed {quantity} x {selected_item_name} from your order.")
                        return
                    else:
                        break  # Break if the item is found but quantity is too high

            # If the function hasn't returned by this point, the item wasn't found or the quantity was too high
            gz.error("Remove Error", "Item not found or quantity exceeds the amount in the order.")
        except ValueError:
            gz.error("Input Error", "Please enter a valid quantity.")

    def check_out(self):
        if not self.order.items:  # Check if order is empty
            gz.error("Check Out Error", "No items in the order.")
            return
        if gz.yesno("Confirm Checkout", "Are you sure you want to checkout?"):
            # Display the final order summary
            final_summary = self.order.get_summary()
            gz.info("Final Order", final_summary)
            self.reset_application()

    def reset_application(self):
        # reset the order
        self.order = Order()
        self.update_order_summary_box()
        self.item_list.clear()
        self.description_box.clear()
        self.quantity_box.clear()
        self.category_combo.value = "SELECT A CATEGORY"

    def show_order_summary(self):
        summary = self.order.get_summary()
        gz.info("Order Summary", summary)

    def display(self):
        self.app.display()
