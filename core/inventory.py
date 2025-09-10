from core.database import DB

class InventoryManager:
    def __init__(self):
        self.db = DB()
        self.linked_items = {}  # key: item name, value: item dict

    def search_item(self, name):
        """Search for item in store inventory."""
        result = self.db.get_item_by_name(name)
        if result:
            item_name, rate, tax = result
            return {
                "name": item_name,
                "rate": rate,
                "tax": tax
            }
        return None  # Not found

    def add_or_update_item(self, name, rate, tax, quantity):
        """Add item to linked list or update quantity if already added."""
        if name in self.linked_items:
            self.linked_items[name]["quantity"] += quantity
        else:
            self.linked_items[name] = {
                "name": name,
                "rate": rate,
                "tax": tax,
                "quantity": quantity
            }

    def get_linked_items(self):
        """Return all items added to the invoice."""
        return list(self.linked_items.values())

    def clear_items(self):
        """Reset the linked items list."""
        self.linked_items.clear()

    def remove_item(self, name):
        """Remove item from linked_items by name."""
        name = name.lower()
        keys_to_remove = [key for key in self.linked_items if key.lower() == name]
        for key in keys_to_remove:
            del self.linked_items[key]
    
    def search_matches(self, query):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM items WHERE LOWER(name) LIKE ?", (f"%{query}%",))
        return [row[0] for row in cursor.fetchall()]

