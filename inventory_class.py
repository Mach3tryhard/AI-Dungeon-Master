
class Inventory:
    def __init__(self, items: list = None, gold: int = 0):
        self.items = items if items is not None else []
        self.gold = gold

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def add_gold(self, amount: int):
        self.gold += amount

    def remove_gold(self, amount: int):
        if self.gold >= amount:
            self.gold -= amount