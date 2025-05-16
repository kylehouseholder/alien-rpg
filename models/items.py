from typing import Dict, List, Optional, Union, Set
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

# --- Wearable Slots ---
WEARABLE_SLOTS = [
    "head", "face", "torso", "left_arm", "right_arm", "back", "waist", "left_leg", "right_leg", "feet"
]

@dataclass
class WearableItem:
    name: str
    armor_rating: int = 0 # Base dice rolled to resist incoming damage from attacks
    encumbrance: float = 0.0 # Weight of item in encumbrance units (0.25, 0.5, 1, 2...); None = not carriable
    coverage_slots: List[str] = field(default_factory=list) # Body parts covered; used to prevent overlapping gear
    suit_compatible: bool = True # If true, this item is compatible with suits
    cost: int = 0 # Market value in local currency (e.g., WYD or USD)
    lore: Optional[str] = None # In-universe description or flavor text for immersion or inspection
    sealed: bool = False # True if suit provides vacuum protection (required for spacewalks, prevents decompression damage)
    environment_type: Optional[str] = None # Primary environmental protection type (e.g., "vacuum", "radiation")
    air_supply_rating: Optional[int] = None # Consumable air supply; rolled as Stress Dice, depletes on 1s
    power_supply_rating: Optional[int] = None # Internal power source; Stress Dice are rolled per shift in extreme environments to determine depletion
    hazard_resistances: List[str] = field(default_factory=list) # Specific resistances to hazards like heat, acid, gas, etc.
    built_in_systems: List[str] = field(default_factory=list) # Embedded equipment (e.g., HUD, comms, sensors, camera, lights)
    skill_modifiers: Optional[Dict[str, int]] = None # Passive skill bonuses or penalties while wearing (e.g., +3 SURVIVAL, -1 MOBILITY)
    attribute_modifiers: Optional[Dict[str, int]] = None # Global attribute modifiers (e.g., {"STRENGTH": +1} affects all STRENGTH-based rolls)
    conditional_modifiers: Optional[List[Dict[str, str]]] = None # Conditional bonuses that only apply in certain contexts (e.g., +2 MOBILITY in matching terrain for Ghillie suits)
    conditional_deflection: Optional[Dict[str, str]] = None # Special triggered effects against specific attacks (e.g., BiMex shades deflecting lasers on a 6)
    locator_linked: bool = False # If true, this item broadcasts location to a paired tracking device (e.g., PDT/L set)
    activated_encumbrance: Optional[float] = None # Expanded or deployed weight, if it differs from base (e.g., survival shelters or deployed gear)
    carry_bonus: Optional[int] = None # Increases the user's carrying capacity (e.g., powered suits or packs like the IMP)
    post_use_requirement: Optional[str] = None # Any mandatory condition after suit use (e.g., "requires decompression chamber")
    zero_g_thrusters: bool = False # Enables the wearer to move freely in zero-G without tethers
    required_skills: Optional[Dict[str, int]] = None # Minimum skills required to use this item (e.g., {"HEAVY MACHINERY": 2})
    built_in_weapon_damage: Optional[int] = None # Base melee damage dealt by integrated close combat systems (e.g., power claws)
    integrated_weapon: Optional[str] = None # Name of integrated weapon system, if any (e.g., "AK-104")
    integrated_in: Optional[str] = None # Indicates if the item is part of another system or armor set (e.g., "M3 Personnel Armor")
    provides_cover: bool = False # If true, this item grants mechanical cover when deployed (e.g., riot shield)
    fall_protection: Optional[int] = None # Reduces damage taken from falling by this amount
    radiation_absorption_dice: Optional[int] = None # If set, roll this many Base Dice when exposed to radiation; any SIXES cancel Radiation Points
    special_deflection_dice: Optional[int] = None # Dice rolled to deflect specific attack types (e.g., explosive, energy, fire)
    special_deflection_condition: Optional[str] = None # Trigger condition for the special deflection (e.g., "energy/fire/radiation only")
    modifiers: Optional[Dict[str, Union[str, int, float, dict, list, bool]]] = None  # For rare/special fields only
    
    def get_armor_per_slot(self) -> Dict[str, int]:
        return {slot: self.armor_rating for slot in self.coverage_slots}
    def get_encumbrance(self) -> float:
        return self.encumbrance

# --- Clothing ---
@dataclass
class ClothingItem(WearableItem):
    def __post_init__(self):
        # Clothing always covers all 6 main body parts
        self.coverage_slots = ["torso", "left_arm", "right_arm", "left_leg", "right_leg"]
        self.suit_compatible = False

# --- Armor ---
@dataclass
class ArmorItem(WearableItem):
    pass  # Modular, can cover any slot(s)

# --- Suit ---
@dataclass
class SuitItem(WearableItem):
    suit_allows_accessory_slots: Optional[List[str]] = None
    def __post_init__(self):
        # Suits cover all main body parts, hands, feet, head
        self.coverage_slots = ["torso", "left_arm", "right_arm", "left_leg", "right_leg", "head", "feet"]
        self.suit_compatible = False

# --- Accessory ---
@dataclass
class AccessoryItem(WearableItem):
    slot: str = ""
    suit_compatible: bool = True
    def __post_init__(self):
        self.coverage_slots = [self.slot] 