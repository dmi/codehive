class Item:
    def __init__(self, name, quantity=1, stackable=True):
        self.name = name
        self.quantity = quantity
        self.stackable = stackable

    def use(self):
        print(f"Использовано {self.name}")