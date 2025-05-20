# Character creation helper functions moved from main.py

from models.items import Item, ConsumableItem
from models.dice import DiceRoll
from models.wearables import all_wearable_items
from models.weapons import all_weapon_items
from models.weapon_item import WeaponItem

# --- Formatting helpers ---
def format_attribute_bar(value, is_key=False):
    stars = " " + " ".join("*" * value)  
    spaces = " " * (11 - len(stars))
    if is_key:
        return f"{{{stars}{spaces}}}" 
    return f"[{stars}{spaces}]"

def format_skill_bar(value):
    stars = " " + " ".join("*" * value)
    spaces = " " * (11 - len(stars))  
    return f"[{stars}{spaces}]"

# --- Gear helpers ---
def get_paired_gear(gear_list: list) -> list[tuple[str, str]]:
    """Identify pairs of mutually exclusive gear items. Each career has 8 items organized into 4 pairs."""
    pairs = []
    for i in range(0, len(gear_list), 2):
        if i + 1 < len(gear_list):
            pairs.append((gear_list[i], gear_list[i + 1]))
    return pairs

def get_article_for_item(item_name: str) -> str:
    """Add the appropriate article to an item name based on its characteristics."""
    no_article_prefixes = [
        "1d6", "2d6", "3d6", "4d6", "5d6", "6d6",  # Dice rolls
        "1d3", "2d3", "3d3", "4d3", "5d3", "6d3",
        "1d4", "2d4", "3d4", "4d4", "5d4", "6d4",
        "1d8", "2d8", "3d8", "4d8", "5d8", "6d8",
        "1d10", "2d10", "3d10", "4d10", "5d10", "6d10",
        "1d12", "2d12", "3d12", "4d12", "5d12", "6d12",
        "1d20", "2d20", "3d20", "4d20", "5d20", "6d20",
        "1d100", "2d100", "3d100", "4d100", "5d100", "6d100",
        "1 ", "2 ", "3 ", "4 ", "5 ", "6 ",  # Simple quantities
        "1x", "2x", "3x", "4x", "5x", "6x"
    ]
    for prefix in no_article_prefixes:
        if item_name.startswith(prefix):
            return item_name
    definite_articles = [
        "M4A3", "M41A", "M56A2", "M314", "M3", "M72", ".357", "Armat",
        "Rexim", "Watatsumi", "B9", "G2", "Model", "Pump-Action",
        "IRC", "PR-PUT", "Seegson", "Samani", "Daihotai",
        "Personal", "Hand", "Maintenance", "Hi-beam",
        "Binoculars", "Cards", "Drugs", "Pills", "Tools", "Grenades",
        "Surgical", "Digital", "Neuro", "Eco", "Recreational"
    ]
    for prefix in definite_articles:
        if item_name.startswith(prefix):
            return f"the {item_name}"
    an_prefixes = ["EVA", "IRC", "IFF", "Eco", "Electronic"]
    for prefix in an_prefixes:
        if item_name.startswith(prefix):
            return f"an {item_name}"
    return f"a {item_name}"

def find_wearable_by_name(name):
    for item in all_wearable_items:
        if item.name.lower() == name.lower():
            return item
    return None

def find_weapon_by_name(name):
    for item in all_weapon_items:
        if item.name.lower() == name.lower():
            return item
    return None

def handle_dice_roll_item(item_name: str) -> tuple[str, int]:
    import re
    dice_pattern = r'(\d+d\d+)\s+(?:doses of|rounds of|)\s*(.+)'
    match = re.match(dice_pattern, item_name)
    if match:
        dice_expr, item_name = match.groups()
        quantity = DiceRoll.roll(dice_expr)
        return item_name.strip(), quantity
    return item_name, 1 

# --- Weapon display helpers ---
def get_skill_and_attr(weapon):
    if hasattr(weapon, 'weapon_class') and weapon.weapon_class in ["pistol", "rifle", "heavy", "launcher", "grenade", "ammunition", "chemical"]:
        return "Ranged Combat", "Agility"
    elif hasattr(weapon, 'weapon_class') and weapon.weapon_class in ["melee"]:
        return "Close Combat", "Strength"
    else:
        return "Ranged Combat", "Agility"

def get_type_icon(weapon):
    type_map = {
        "ballistic": "🏹",
        "energy": "⚡",
        "melee": "🗡️",
        "fire": "🔥",
        "blast": "💣",
        "stun": "💫",
        "piercing": "🗡️",
        "impact": "🔨",
        "chemical": "☣️",
        "special": "✨",
        "kinetic": "🔫",
        "physical": "🛡️"
    }
    return type_map.get(getattr(weapon, 'damage_type', None), "🔪")

def get_ammo_icon(weapon):
    if getattr(weapon, "uses_ammo", False):
        return "🧱🧱🧱"  # Placeholder: could show actual ammo count if tracked
    elif getattr(weapon, "power_supply", None):
        return f"🔋{weapon.power_supply}"
    elif getattr(weapon, "single_shot", False):
        return "🧱 (reloads after each shot)"
    else:
        return "∞"

def get_modifiers(weapon):
    mods = []
    if getattr(weapon, "armor_effect", None):
        mods.append(weapon.armor_effect.replace("_", " ").title())
    if getattr(weapon, "full_auto", False):
        mods.append("Full Auto")
    if getattr(weapon, "special_effect", None):
        mods.append(weapon.special_effect)
    return ", ".join(mods) if mods else "None" 