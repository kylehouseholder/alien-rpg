from dataclasses import dataclass, field
from typing import Optional, List
from .items import Item

@dataclass
class WeaponItem(Item):
    """Weapons used in combat, with attributes matching core Alien RPG mechanics."""

    # --- BASIC COMBAT STATS ---
    bonus: int = 0  # Modifier applied to CLOSE COMBAT or RANGED COMBAT rolls
    damage: int = 0  # Base damage dealt on a successful hit (extra successes add more damage)
    range: str = "Short"  # Maximum effective range: "Engaged", "Short", "Medium", "Long", or "Extreme"
    weight: Optional[int] = None  # Inventory weight; None means too heavy to carry
    cost: int = 0  # Typical price in UA dollars, adjustable for market conditions

    # --- LORE & DESCRIPTION ---
    lore: Optional[str] = None  # Narrative description or blurb for roleplaying or inspection purposes
    
    # --- CLASSIFICATION ---
    weapon_class: str = "melee"  # Weapon type classification: melee, pistol, rifle, heavy, throwable, etc.
    damage_type: str = "melee"  # Damage type classification: melee, ballistic, blast, fire, acid, radiation, stun, etc.

    # --- FIRING MODES & AMMO ---
    full_auto: bool = False  # True if the weapon can fire in fully automatic mode
    uses_ammo: bool = False  # True if the weapon requires reloads and can run out of ammo
    ammo_types: Optional[List[str]] = None  # List of compatible ammo types, e.g. ["frag", "smoke", "flash"]
    single_shot: bool = False  # True if weapon must be reloaded after every shot
    power_supply: Optional[int] = None  # Maximum power supply level when fully charged (None if not powered)

    # --- DAMAGE EFFECTS ---
    blast_power: Optional[int] = None  # Number of dice rolled for each target in blast radius
    fire_intensity: Optional[int] = None  # If set, fire attack intensity instead of normal damage
    fire_on_hit: bool = False  # If True, fire_intensity applies only on successful hit
    inflicts_condition: Optional[str] = None  # Inflicted condition (disease, poison, radiation, nerve_agent)
    special_effect: Optional[str] = None  # Additional effect on hit (stun, shock, flashbang, etc.)

    # --- ARMOR & DAMAGE HANDLING ---
    armor_effect: Optional[str] = None  # "armor_piercing", "armor_doubled", or None
    max_damage: Optional[int] = None  # Max damage per hit (None if unlimited)
    range_damage_falloff: Optional[str] = None  # Damage falloff description (e.g. "-1 per range band beyond Short")
    direct_target_bonus: Optional[str] = None  # Bonus/effect on direct target (e.g. +2 damage vs target)

    # --- DETONATION, DEPLOYMENT & AREA EFFECTS ---
    detonation_trigger: Optional[str] = None  # Trigger method (timer, remote, proximity)
    area_effect: Optional[str] = None  # Description of area effect (illumination, smoke, gas, suppression)
    persistent_effect: Optional[str] = None  # Lingering effects (e.g. burning zone, gas hazard)

    # --- ATTACHMENTS & INTEGRATION ---
    secondary_weapon: Optional[str] = None  # Integrated secondary weapon (e.g. grenade launcher)
    integrated_in: Optional[str] = None  # If part of another item (e.g. CCC5 Combat Suit)

    # --- VULNERABILITIES & MALFUNCTIONS ---
    vulnerable_component: Optional[str] = None  # Weak point if destroyed (e.g. ammo pack blast)
    overload_risk: Optional[str] = None  # Overuse risk (e.g. forced fire → explode)
    malfunction_risk: Optional[str] = None  # Maintenance or hazard risk (e.g. uncleaned → stun user)

    # --- OPERATIONAL TRAITS ---
    autonomous: bool = False  # True if weapon operates without user (e.g. sentry gun)
    autonomous_skill: Optional[int] = None  # Autonomous fire skill
    hidden: Optional[str] = None  # Description of concealment (e.g. "Observation to detect mine")
    alternate_fire_mode: Optional[str] = None  # Alternate fire description (e.g. burst, stun, focused beam)
    user_condition_penalty: Optional[str] = None  # Penalty based on user attributes (e.g. STR < 3 → -1 to RANGED COMBAT)
    critical_override: Optional[str] = None  # Forced critical injury result (e.g. "Critical #15 on crit hit")

    def __str__(self) -> str:
        range_display = f"Range: {self.range}" if self.range else ""
        weight_display = f"Weight: {self.weight}" if self.weight is not None else "Weight: Uncarryable"
        return f"{self.name} (Bonus: {self.bonus}, Damage: {self.damage}, {range_display}, {weight_display})"
