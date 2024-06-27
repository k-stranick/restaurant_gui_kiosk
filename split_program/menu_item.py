# MenuItem class definition
class MenuItem:
    def __init__(self, item_id, name, category, price, description):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"
