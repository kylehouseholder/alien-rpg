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
    power_supply: Optional[int] = None  # Maximum power supply level when fully charged (None if weapon does not use power)
    special_ammo_effect: Optional[str] = None  # Name or description of special ammo effect (e.g. "dirty_bullets")

    # --- DAMAGE EFFECTS ---
    blast_power: Optional[int] = None  # Number of dice rolled for each target in blast radius
    fire_intensity: Optional[int] = None  # If set, fire attack intensity in addition to normal damage (if any); otherwise, fire damage only
    fire_on_hit: bool = False  # If True, fire_intensity applies only on successful hit
    inflicts_condition: Optional[str] = None  # Inflicted condition (disease, poison, radiation, nerve_agent)
    special_effect: Optional[str] = None  # Description of additional effect on hit (e.g., "stun (STAMINA -2, lose slow action for 1 round)")
    grappling: bool = False  # True if weapon can tether or pull targets/self on hit

    # --- ARMOR & DAMAGE HANDLING ---
    armor_effect: Optional[str] = None  # Special armor interaction: "armor_piercing", "armor_doubled", or None
    max_damage: Optional[int] = None  # Max damage per hit (None if unlimited)
    range_damage_falloff: Optional[str] = None  # Damage falloff description (e.g. "-1 per range band beyond Short")
    direct_target_bonus: Optional[str] = None  # Bonus or effect against direct target (e.g. "+2 damage and armor piercing vs target surface")

    # --- DETONATION, DEPLOYMENT & AREA EFFECTS ---
    detonation_trigger: Optional[str] = None  # Description of trigger for detonation (e.g., "1 round delay or movement")
    area_effect: Optional[str] = None  # Description of area effect (illumination, smoke, gas, suppression)
    persistent_effect: Optional[str] = None  # Description of lingering effects, e.g. "Suffer 1 damage and +1 Stress per round until cured"

    # --- ATTACHMENTS & INTEGRATION ---
    secondary_weapon: Optional[str] = None  # Integrated secondary weapon (e.g. grenade launcher)
    integrated_in: Optional[str] = None  # If part of another item (e.g. CCC5 Combat Suit)

    # --- VULNERABILITIES & MALFUNCTIONS ---
    vulnerable_component: Optional[str] = None  # Description of vulnerable component and effect if destroyed (e.g. "Ammo pack explosion (Blast 9)")
    overload_risk: Optional[str] = None  # Description of overload risk and consequence (e.g. "On forced fire, roll Stress Die. On 1, explode (Blast 12)")
    malfunction_risk: Optional[str] = None  # Description of malfunction risk and consequence, e.g. "If 2+ Stress ONES rolled, shooter is stunned"

    # --- OPERATIONAL TRAITS ---
    autonomous: bool = False  # True if weapon operates without user (e.g., sentry gun)
    autonomous_skill: Optional[int] = None  # Autonomous fire skill
    hidden: Optional[str] = None  # Description of concealment or spotting rules, e.g. "Observation roll required to detect
    alternate_fire_mode: Optional[str] = None  # Description of alternate fire option, e.g. "Focused fire: +3 damage, Extreme range, no full auto"
    user_condition_penalty: Optional[str] = None  # Description of penalties based on user attributes (e.g. STR < 3 → -1 to RANGED COMBAT)
    critical_override: Optional[str] = None  # Forced critical injury result (e.g. "Critical #15 on crit hit")
    recharge_time: Optional[str] = None  # Description of recharge/delay mechanic (e.g. "2 rounds between firing")

    def __str__(self) -> str:
        range_display = f"Range: {self.range}" if self.range else ""
        weight_display = f"Weight: {self.weight}" if self.weight is not None else "Weight: Uncarryable"
        return f"{self.name} (Bonus: {self.bonus}, Damage: {self.damage}, {range_display}, {weight_display})"

########################################################################################

### class WeaponItem(Item):
###    """Weapons used in combat, with attributes matching core Alien RPG mechanics."""
###    bonus: int = 0  # Modifier applied to CLOSE COMBAT or RANGED COMBAT rolls
###    damage: int = 0  # Base damage dealt on a successful hit (extra successes add more damage)
###    range: str = "Short"  # Maximum effective range: "Engaged", "Short", "Medium", "Long", or "Extreme"
###    weight: Optional[int] = None  # Inventory weight; None means too heavy to carry
###    cost: int = 0  # Typical price in UA dollars, adjustable for market conditions
###    weapon_class: str = "melee"  # Weapon type classification: melee, pistol, rifle, heavy, throwable, etc.
###    damage_type: str = "melee"  # Damage type classification: melee, ballistic, blast, fire, acid, radiation, stun, etc.
###    full_auto: bool = False  # True if the weapon can fire in fully automatic mode
###    uses_ammo: bool = False  # True if the weapon requires reloads and can run out of ammo
###    blast_power: Optional[int] = None  # Number of dice rolled for each target in blast radius (if applicable)
###    fire_intensity: Optional[int] = None  # If set, target suffers fire attack with this intensity instead of normal damage
###    fire_on_hit: bool = False  # If True, fire_intensity is applied only on a successful hit
###    inflicts_condition: Optional[str] = None  # Name of condition inflicted on hit, e.g. disease, poison, radiation
###    armor_effect: Optional[str] = None  # Special armor interaction: None, "armor_piercing", or "armor_doubled"
###    single_shot: bool = False  # True if weapon must be reloaded after every shot
###    power_supply: Optional[int] = None  # Maximum power supply level when fully charged (None if weapon does not use power)
###    grappling: bool = False  # True if weapon can tether or pull targets/self on hit
###    secondary_weapon: Optional[str] = None  # Reference to integrated secondary weapon, if applicable
###    special_ammo_effect: Optional[str] = None  # Name or description of special ammo effect, e.g. "dirty_bullets"
###    ammo_types: Optional[List[str]] = None  # List of compatible ammo types, e.g. ["frag", "smoke", "flash", "electroshock"]
###    autonomous: bool = False  # True if weapon can fire on its own without a user (automated sentry)
###    autonomous_skill: Optional[int] = None  # Skill rating when firing autonomously (None if not applicable)
###    special_effect: Optional[str] = None  # Description of a special effect on hit, e.g. "Stun (STAMINA -2, lose slow action for 1 round)"
###    max_damage: Optional[int] = None  # Maximum damage this weapon can deal per hit (None if unlimited)
###    detonation_trigger: Optional[str] = None  # Description of trigger for detonation, e.g. "1 round delay or movement"
###    integrated_in: Optional[str] = None  # If set, indicates this weapon is part of another object (e.g. "CCC5 Combat Compression Suit")
###    vulnerable_component: Optional[str] = None  # Description of vulnerable component and effect if destroyed (e.g. "Ammo pack explosion (Blast 9)")
###    range_damage_falloff: Optional[str] = None  # Description of damage falloff, e.g. "-1 damage per range band beyond Short"
###    alternate_fire_mode: Optional[str] = None  # Description of alternate fire option, e.g. "Focused fire: +3 damage, Extreme range, no full auto"
###    recharge_time: Optional[str] = None  # Description of recharge/delay mechanic, e.g. "2 rounds between firing"
###    overload_risk: Optional[str] = None  # Description of overload risk and consequence, e.g. "On forced fire, roll Stress Die. On 1, explode (Blast 12)"
###    area_effect: Optional[str] = None  # Description of area effect, e.g. "Illuminates zone for D6 rounds"
###    critical_override: Optional[str] = None  # Description of critical injury special rule, e.g. "Critical #15 on crit hit"
###    direct_target_bonus: Optional[str] = None  # Bonus or effect against direct target (e.g. "+2 damage and armor piercing vs target surface")
###    hidden: Optional[str] = None  # Description of concealment or spotting rules, e.g. "Observation roll required to detect"
###    persistent_effect: Optional[str] = None  # Description of lingering effects, e.g. "Suffer 1 damage and +1 Stress per round until cured"
###    user_condition_penalty: Optional[str] = None  # Description of penalties based on user traits, e.g. "Users with STR < 3 suffer -1 RANGED COMBAT"
###    malfunction_risk: Optional[str] = None  # Description of malfunction risk and consequence, e.g. "If 2+ Stress ONES rolled, shooter is stunned"



