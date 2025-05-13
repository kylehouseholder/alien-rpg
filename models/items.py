from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from .dice import DiceRoll

@dataclass
class Item:
    """Base class for all items in the game"""
    name: str
    description: str = ""
    quantity: int = 1
    stackable: bool = True
    condition: int = 1
    price: int = 0  # Base price of the item
    
    def __str__(self) -> str:
        if self.stackable == True and self.quantity:
            return f"{self.name} (x{self.quantity})"
        if self.quantity:
            return self.name
        raise ValueError("No item exists for this reference.")

    def get_value(self) -> int:
        """Get the current value of the item based on condition"""
        return round(self.condition * self.price)

@dataclass
class ConsumableItem(Item):
    """Items that can be used/consumed like medical supplies"""
    uses: int = 1
    dice_expression: Optional[str] = None  # For items that spawn with random quantities
    
    def __post_init__(self):
        if self.dice_expression:
            self.uses = DiceRoll.roll(self.dice_expression)
            
    def use(self) -> bool:
        """Use one charge of the item. Returns False if no uses remain."""
        if self.uses <= 0:
            return False
        self.uses -= 1
        return True

@dataclass 
class Inventory:
    """Manages a collection of items"""
    items: List[Item] = field(default_factory=list)
    
    def add_item(self, item: Item) -> None:
        """Add an item to inventory, stacking if possible"""
        if item.stackable:
            for existing_item in self.items:
                if existing_item.name == item.name:
                    existing_item.quantity += item.quantity
                    return
        # Only append if we didn't find a matching item to stack with
        self.items.append(item)
        
    def remove_item(self, item_name: str, quantity: int = 1) -> Optional[Item]:
        """Remove an item from inventory. Returns the removed item or None if not found."""
        for i, item in enumerate(self.items):
            if item.name == item_name:
                if item.quantity <= quantity:
                    return self.items.pop(i)
                item.quantity -= quantity
                new_item = type(item)(name=item.name, quantity=quantity)
                return new_item
        return None
        
    def get_item(self, item_name: str) -> Optional[Item]:
        """Get an item without removing it"""
        for item in self.items:
            if item.name == item_name:
                return item
        return None 