from dataclasses import dataclass, field
from typing import Optional, List, Dict
from .items import Item

@dataclass
class EquipmentItem(Item):
    name: str  # Name of the item, used for identification and display
    cost: int  # Market or requisition cost in UA dollars
    weight: Optional[float] = 0  # How much inventory space the item takes (0 = negligible)
    description: Optional[str] = None  # Short lore-based or mechanical summary of the item
    skill_modifiers: Optional[Dict[str, int]] = None  # Dict mapping skill names to bonus values (e.g., {"COMTECH": +1})
    skill_requirement: Optional[str] = None  # Skill roll required to use the item (e.g., "COMTECH" means COMTECH roll)
    usage_tags: List[str] = field(default_factory=list)  # Functional categories (e.g., ["diagnostic", "communications"])
    slot: Optional[str] = None  # Location on body or inventory where item is equipped (e.g., "hand", "wrist", "implant")
    power_supply_rating: Optional[int] = None  # Total power charge level when fully powered
    requires_power_roll: bool = False  # Whether a Power Supply roll must be made after each use
    consumable: bool = False  # If True, the item is depleted or used up after a number of uses
    capacity_bonus: Optional[int] = None  # Additional items the player can carry with this item equipped (e.g., backpack)
    sensor_capabilities: Optional[List[str]] = None  # Types of detection supported (e.g., ["radiation", "motion"])
    weapon_properties: Optional[Dict[str, any]] = None  # If the equipment can also function as a weapon (e.g., {"bonus": +1, "damage": 2})
    movement_bonus: Optional[Dict[str, int]] = None  # E.g., {"speed": 3} for equipment like parafoils
    environmental_effects: Optional[Dict[str, any]] = None  # Dict for effects like illumination, stress induction, heat resistance
    mobility_bonus: Optional[int] = None  # Bonus to MOBILITY rolls in specific scenarios (e.g., winch climbing aid)
    detection_modifier: Optional[Dict[str, int]] = None  # Bonuses or penalties to being seen or targeted (e.g., -1 OBSERVATION)

@dataclass
class MedicalItem(EquipmentItem):
    medical_aid_level: Optional[int] = None  # Skill level the item performs medical actions with, if automated
    programmable: bool = False  # Whether the item requires a COMTECH roll to configure or initiate
    limited_uses: Optional[int] = None  # Number of uses available before the item is expended (if not power-based)

@dataclass
class PharmaceuticalItem(EquipmentItem):
    effects: List[str] = field(default_factory=list)  # Text descriptions of mechanical effects (e.g., "+1 STRESS")
    addictive: bool = False  # Whether repeated use has in-world addiction consequences
    black_market: bool = False  # Whether the substance is illegal, controlled, or black-market restricted

@dataclass
class ConsumableItem(EquipmentItem):
    supply_type: Optional[str] = None  # Type of consumable it increases: "food", "water", or both
    stress_effect: Optional[int] = None  # STRESS LEVEL increase or decrease (e.g., +1 for coffee, -1 for alcohol)
    attribute_penalties: Optional[Dict[str, int]] = None  # Temporary penalties (e.g., WITS: -1 from alcohol)
    bonus_effects: List[str] = field(default_factory=list)  # Additional narrative or conditional mechanical notes
    specialty: Optional[bool] = False  # Whether it's a gourmet/specialty item (e.g., colony cuisine)

def __str__(self) -> str:
    weight_display = f"Weight: {self.encumbrance}" if self.encumbrance is not None else "Weight: Uncarryable"
    power_display = f"Power: {self.power_supply_rating}" if self.power_supply_rating else ""
    tags_display = f"Tags: {', '.join(self.usage_tags)}" if self.usage_tags else ""
    return f"{self.name} ({weight_display}{', ' if power_display else ''}{power_display}{', ' if tags_display else ''}{tags_display})"
