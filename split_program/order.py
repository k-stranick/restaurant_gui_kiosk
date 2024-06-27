# Order class definition
class Order:
    def __init__(self):
        self.items = {}
        self.total = 0

    def add_item(self, menu_item, quantity):
        if menu_item not in self.items:
            self.items[menu_item] = 0
        self.items[menu_item] += quantity
        self.total += menu_item.price * quantity

    def remove_item(self, menu_item, quantity):
        if menu_item in self.items:
            self.items[menu_item] -= quantity
            if self.items[menu_item] <= 0:
                del self.items[menu_item]
            self.total -= menu_item.price * quantity  # Adjust the total price
            if self.total < 0:
                self.total = 0  # Prevent negative totals

    def get_summary(self):
        summary = "\nOrder Summary:\n"
        for item, quantity in self.items.items():
            item_total = quantity * item.price
            summary += f"{item.name} x {quantity} - ${item_total:.2f}\n"
        summary += f"\nTotal: ${self.total:.2f}"
        return summary