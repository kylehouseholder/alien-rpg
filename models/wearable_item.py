from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .items import ClothingItem, ArmorItem, SuitItem, AccessoryItem, WearableItem, WEARABLE_SLOTS

@dataclass
class WearableLoadout:
    """Manages a character's equipped wearables, including clothing, armor, suits, and accessories."""
    clothing: Optional[ClothingItem] = None
    armor: List[ArmorItem] = field(default_factory=list)
    suit: Optional[SuitItem] = None
    accessories: List[AccessoryItem] = field(default_factory=list)
    slots: Dict[str, Optional[WearableItem]] = field(default_factory=lambda: {slot: None for slot in WEARABLE_SLOTS})
    
    def equip(self, item: WearableItem) -> bool:
        """Equip a wearable item. Returns True if successful."""
        # Handle suits (mutually exclusive with clothing/armor)
        if isinstance(item, SuitItem):
            if self.suit:
                return False  # Only one suit
            self.suit = item
            for slot in item.coverage_slots:
                self.slots[slot] = item
            # Remove all armor (ignored while suit is on)
            self.armor.clear()
            return True
        # Handle clothing (mutually exclusive with suit)
        if isinstance(item, ClothingItem):
            if self.suit:
                return False
            if self.clothing:
                return False
            self.clothing = item
            for slot in item.coverage_slots:
                self.slots[slot] = item
            return True
        # Handle armor (mutually exclusive with suit)
        if isinstance(item, ArmorItem):
            if self.suit:
                return False
            # Check for slot overlap
            for slot in item.coverage_slots:
                if self.slots[slot] and not isinstance(self.slots[slot], ClothingItem):
                    return False
            self.armor.append(item)
            for slot in item.coverage_slots:
                self.slots[slot] = item
            return True
        # Handle accessories
        if isinstance(item, AccessoryItem):
            # If suit is on, check compatibility
            if self.suit and (not item.suit_compatible or (self.suit.suit_allows_accessory_slots and item.slot not in self.suit.suit_allows_accessory_slots)):
                return False
            # Only one per slot
            for acc in self.accessories:
                if acc.slot == item.slot:
                    return False
            self.accessories.append(item)
            self.slots[item.slot] = item
            return True
        return False
    
    def unequip(self, item: WearableItem) -> bool:
        """Unequip a wearable item. Returns True if successful."""
        if isinstance(item, SuitItem) and self.suit == item:
            for slot in item.coverage_slots:
                if self.slots[slot] == item:
                    self.slots[slot] = None
            self.suit = None
            return True
        if isinstance(item, ClothingItem) and self.clothing == item:
            for slot in item.coverage_slots:
                if self.slots[slot] == item:
                    self.slots[slot] = None
            self.clothing = None
            return True
        if isinstance(item, ArmorItem) and item in self.armor:
            for slot in item.coverage_slots:
                if self.slots[slot] == item:
                    self.slots[slot] = None
            self.armor.remove(item)
            return True
        if isinstance(item, AccessoryItem) and item in self.accessories:
            if self.slots[item.slot] == item:
                self.slots[item.slot] = None
            self.accessories.remove(item)
            return True
        return False
    
    def get_armor_per_slot(self) -> Dict[str, int]:
        """Calculate armor rating for each body slot."""
        armor_per_slot = {slot: 0 for slot in WEARABLE_SLOTS}
        # If suit is on, only suit AR counts
        if self.suit:
            for slot in self.suit.coverage_slots:
                armor_per_slot[slot] = self.suit.armor_rating
            return armor_per_slot
        # Otherwise, sum armor from armor items
        for armor in self.armor:
            for slot in armor.coverage_slots:
                armor_per_slot[slot] += armor.armor_rating
        # Clothing AR: only add to torso (flat bonus)
        if self.clothing and self.clothing.armor_rating > 0:
            armor_per_slot["torso"] += self.clothing.armor_rating
        # Accessories that provide armor
        for acc in self.accessories:
            for slot in acc.coverage_slots:
                armor_per_slot[slot] += acc.armor_rating
        return armor_per_slot
    
    def get_total_encumbrance(self) -> float:
        """Calculate total encumbrance from all equipped items."""
        total = 0.0
        if self.suit:
            total += self.suit.encumbrance
        if self.clothing:
            total += self.clothing.encumbrance
        for armor in self.armor:
            total += armor.encumbrance
        for acc in self.accessories:
            total += acc.encumbrance
        return total
    
    def get_carry_bonus(self) -> int:
        """Calculate total carry bonus from equipped items."""
        bonus = 0
        for acc in self.accessories:
            if acc.carry_bonus:
                bonus += acc.carry_bonus
        return bonus
    
    def display_loadout(self) -> str:
        """Return a formatted string showing the current loadout."""
        lines = [">> LOADOUT <<"]
        
        if self.clothing:
            lines.append(f"\nClothing: {self.clothing.name}")
            if self.clothing.armor_rating > 0:
                lines.append(f"Armor Rating: {self.clothing.armor_rating}")
            if self.clothing.encumbrance > 0:
                lines.append(f"Encumbrance: {self.clothing.encumbrance}")
        
        if self.armor:
            lines.append("\nArmor:")
            for item in self.armor:
                lines.append(f"• {item.name}")
                if item.armor_rating > 0:
                    lines.append(f"  Armor Rating: {item.armor_rating}")
                if item.encumbrance > 0:
                    lines.append(f"  Encumbrance: {item.encumbrance}")
        
        if self.suit:
            lines.append(f"\nSuit: {self.suit.name}")
            if self.suit.armor_rating > 0:
                lines.append(f"Armor Rating: {self.suit.armor_rating}")
            if self.suit.encumbrance > 0:
                lines.append(f"Encumbrance: {self.suit.encumbrance}")
            if self.suit.air_supply_rating > 0:
                lines.append(f"Air Supply: {self.suit.air_supply_rating}")
        
        if self.accessories:
            lines.append("\nAccessories:")
            for item in self.accessories:
                lines.append(f"• {item.name}")
                if item.armor_rating > 0:
                    lines.append(f"  Armor Rating: {item.armor_rating}")
                if item.encumbrance > 0:
                    lines.append(f"  Encumbrance: {item.encumbrance}")
        
        lines.append(f"\nTotal Encumbrance: {self.get_total_encumbrance()}")
        lines.append(f"Carry Bonus: {self.get_carry_bonus()}")
        
        return "\n".join(lines) 