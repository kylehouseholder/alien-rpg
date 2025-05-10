from dataclasses import dataclass, field
from typing import Optional, List, Dict
from .items import Item

@dataclass
class ArmorItem(Item):
    """Armor and clothing that provide protection, insulation, or utility effects."""

    name: str = ""  # Name of the armor item, for display and reference
    cost: int = 0  # Market value in local currency (e.g., WYD or USD)
    lore: Optional[str] = None  # In-universe description or flavor text for immersion or inspection

    # --- DEFENSIVE STATS ---
    armor_rating: int = 0  # Base dice rolled to resist incoming damage from attacks
    fall_protection: Optional[int] = None  # Reduces damage taken from falling by this amount
    radiation_absorption_dice: Optional[int] = None  # If set, roll this many Base Dice when exposed to radiation; any SIXES cancel Radiation Points
    special_deflection_dice: Optional[int] = None  # Dice rolled to deflect specific attack types (e.g., explosive, energy, fire)
    special_deflection_condition: Optional[str] = None  # Trigger condition for the special deflection (e.g., "energy/fire/radiation only")

    # --- SLOT & LAYER SYSTEM ---
    coverage_slots: List[str] = field(default_factory=list)  # Body parts covered; used to prevent overlapping gear
    layer: int = 1  # Determines how deeply the item is worn; prevents stacking (e.g., base layer vs outer armor)

    # --- ENVIRONMENTAL PROTECTION ---
    sealed: bool = False  # True if suit provides vacuum protection (required for spacewalks, prevents decompression damage)
    environment_type: Optional[str] = None  # Primary environmental protection type (e.g., "vacuum", "radiation")
    air_supply_rating: Optional[int] = None  # Consumable air supply; rolled as Stress Dice, depletes on 1s
    power_supply_rating: Optional[int] = None  # Internal power source; Stress Dice are rolled per shift in extreme environments to determine depletion
    hazard_resistances: List[str] = field(default_factory=list)  # Specific resistances to hazards like heat, acid, gas, etc.

    # --- INTEGRATED SYSTEMS & BONUSES ---
    built_in_systems: List[str] = field(default_factory=list)  # Embedded equipment (e.g., HUD, comms, sensors, camera, lights)
    skill_modifiers: Optional[Dict[str, int]] = None  # Passive skill bonuses or penalties while wearing (e.g., +3 SURVIVAL, -1 MOBILITY)
    attribute_modifiers: Optional[Dict[str, int]] = None  # Global attribute modifiers (e.g., {"STRENGTH": +1} affects all STRENGTH-based rolls)
    conditional_modifiers: Optional[List[Dict[str, str]]] = None  # Conditional bonuses that only apply in certain contexts (e.g., +2 MOBILITY in matching terrain for Ghillie suits)
    conditional_deflection: Optional[Dict[str, str]] = None  # Special triggered effects against specific attacks (e.g., BiMex shades deflecting lasers on a 6)
    locator_linked: bool = False  # If true, this item broadcasts location to a paired tracking device (e.g., PDT/L set)

    # --- ENCUMBRANCE EFFECTS ---
    encumbrance: Optional[float] = 1.0  # Weight of item in encumbrance units (0.25, 0.5, 1, 2...); None = not carriable
    activated_encumbrance: Optional[float] = None  # Expanded or deployed weight, if it differs from base (e.g., survival shelters or deployed gear)
    carry_bonus: Optional[int] = None  # Increases the user's carrying capacity (e.g., powered suits or packs like the IMP)

    # --- POST-USE REQUIREMENTS ---
    post_use_requirement: Optional[str] = None  # Any mandatory condition after suit use (e.g., "requires decompression chamber")

    # --- MOBILITY & NAVIGATION ---
    zero_g_thrusters: bool = False  # Enables the wearer to move freely in zero-G without tethers

    # --- USAGE RESTRICTIONS & WEAPONRY ---
    required_skills: Optional[Dict[str, int]] = None  # Minimum skills required to use this item (e.g., {"HEAVY MACHINERY": 2})
    built_in_weapon_damage: Optional[int] = None  # Base melee damage dealt by integrated close combat systems (e.g., power claws)
    integrated_weapon: Optional[str] = None  # Name of integrated weapon system, if any (e.g., "AK-104")
    integrated_in: Optional[str] = None  # Indicates if the item is part of another system or armor set (e.g., "M3 Personnel Armor")

    # --- DEPLOYMENT EFFECTS ---
    provides_cover: bool = False  # If true, this item grants mechanical cover when deployed (e.g., riot shield)

    def __str__(self) -> str:
        return f"{self.name} (Armor Rating: {self.armor_rating}, Coverage: {self.coverage_slots}, Layer: {self.layer})"
