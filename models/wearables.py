from .items import ArmorItem, SuitItem, ClothingItem, AccessoryItem
from models.items import Item, ConsumableItem, Inventory
from models.weapon_item import WeaponItem
from typing import Optional, List

# --- Clothing ---
bdus = ClothingItem(
    name="Battledress Utilities (BDUs)",
    armor_rating=0,
    encumbrance=0.0,
    cost=55,
    lore="Standard camouflage fatigues worn by troops in all environments.",
    coverage_slots=["torso", "left_arm", "right_arm", "left_leg", "right_leg"]
)

ghillie_suit = ClothingItem(
    name="Ghillie Suit",
    armor_rating=0,
    encumbrance=1.0,
    cost=1000,
    lore="Customized camouflage gear designed for stealth in specific terrain.",
    conditional_modifiers=[
        {"skill": "MOBILITY", "modifier": "+2", "condition": "when avoiding detection in appropriate terrain"}
    ],
    built_in_systems=["heat masking", "infrared scatter"],
    coverage_slots=["torso", "left_arm", "right_arm", "left_leg", "right_leg"]
)

# --- Armor ---
m3_personnel_armor = ArmorItem(
    name="M3 Personnel Armor",
    armor_rating=6,
    encumbrance=1.0,
    coverage_slots=["torso", "left_leg", "right_leg"],
    cost=1200,
    lore="Standard-issue body armor worn by Colonial Marines, known for its rugged, tactical design.",
    built_in_systems=["comm unit", "PDT", "vitals monitor", "combat webbing"]
)

kevlar_riot_vest = ArmorItem(
    name="Kevlar Riot Vest",
    armor_rating=4,
    encumbrance=1.0,
    coverage_slots=["torso"],
    cost=600,
    lore="Woven fiber body armor used by colonial law enforcement and security teams.",
    built_in_systems=["comm unit"]
)

# --- Suit ---
irc_mk50_compression_suit = SuitItem(
    name="IRC Mk.50 Compression Suit",
    armor_rating=2,
    encumbrance=1.0,
    cost=15000,
    lore="A dependable, aging vacuum suit still widely used across the Frontier.",
    air_supply_rating=5,
    sealed=True,
    environment_type="vacuum",
    built_in_systems=["comm unit", "HUD", "headlamp", "helmet cam"],
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

eco_survival_suit = SuitItem(
    name="Eco All-World Survival Suit",
    armor_rating=4,
    encumbrance=2.0,
    cost=30000,
    lore="A high-end EVA hardsuit designed for zero-G missions and hostile environments.",
    air_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    hazard_resistances=["extreme cold", "extreme pressure"],
    built_in_systems=["HUD", "helmet cam", "comm unit", "data ports"],
    zero_g_thrusters=True,
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

# --- Accessory ---
marine_backpack = AccessoryItem(
    name="USCMC Field Backpack",
    armor_rating=0,
    encumbrance=0.5,
    slot="back",
    suit_compatible=True,
    cost=100,
    lore="Standard-issue field backpack for Colonial Marines.",
    carry_bonus=2
)

combat_armor_6b90 = ArmorItem(
    name="6B90 Combat Armor",
    armor_rating=6,
    encumbrance=2.0,
    coverage_slots=["head", "torso", "left_arm", "right_arm", "left_leg", "right_leg"],
    cost=1000,
    lore="Heavier than USCMC gear, this bulky UPP armor protects vital areas with tactical oversight.",
    built_in_systems=["comm unit", "tactical camera"]
)

ccc5_compression_suit = SuitItem(
    name="CCC5 Combat Compression Suit",
    armor_rating=2,
    encumbrance=2.0,
    cost=15500,
    lore="An armored vacuum suit with a narrow helmet view and a built-in AK-104 rifle.",
    air_supply_rating=5,
    sealed=True,
    environment_type="vacuum",
    skill_modifiers={"OBSERVATION": -1},
    integrated_weapon="AK-104",
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

bimex_personal_shades = AccessoryItem(
    name="BiMex Personal Shades",
    armor_rating=0,
    encumbrance=0,
    slot="face",
    suit_compatible=True,
    cost=150,
    lore="Stylish, military-issue eyewear designed to shield against battlefield glare and optical hazards.",
    conditional_deflection={
        "trigger": "hit by laser weapon",
        "mechanic": "Roll 1 Base Die; on 6, beam is deflected and damage is negated; item is destroyed"
    },
    coverage_slots=["face"]
)

pdt_locator_set = AccessoryItem(
    name="PDT/L Bracelet and Locator Tube",
    armor_rating=0,
    encumbrance=0.25,
    slot="left_arm",
    suit_compatible=True,
    cost=100,
    lore="A short-range tracking system pairing a wrist-worn transmitter with a directional locator tube.",
    locator_linked=True,
    coverage_slots=["left_arm", "right_arm"]
)

expedition_fatigues = ClothingItem(
    name="Expedition Fatigues",
    armor_rating=0,
    encumbrance=0,
    cost=55,
    lore="Thermal-regulating undersuit designed for frontier exploration in extreme climates.",
    skill_modifiers={"STAMINA": +1},
    hazard_resistances=["heat", "cold", "vacuum"],
    coverage_slots=["torso", "left_arm", "right_arm", "left_leg", "right_leg"]
)

m8a2_thermal_boots = AccessoryItem(
    name="M8A2 Thermal Boots",
    armor_rating=0,
    encumbrance=0,
    slot="feet",
    suit_compatible=True,
    cost=75,
    lore="Insulated boots made for prolonged exposure to freezing temperatures.",
    skill_modifiers={"STAMINA": +1}
)

m11_platypus_fins = AccessoryItem(
    name="M11 Performance Enhanced Platypus Fins",
    armor_rating=0,
    encumbrance=0.5,
    slot="feet",
    suit_compatible=True,
    cost=100,
    lore="Advanced fins engineered for high-performance aquatic movement.",
    conditional_modifiers=[
        {"skill": "MOBILITY", "modifier": "+2", "condition": "when underwater"}
    ]
)

presidium_mk8_se_suit = SuitItem(
    name="Presidium Mark VIII Advanced SE Suit",
    armor_rating=1,
    encumbrance=2.0,
    cost=5000,
    lore="A sleek, reinforced exosuit designed for Weyland-era deep space expeditions.",
    air_supply_rating=3,
    sealed=True,
    environment_type="vacuum",
    attribute_modifiers={"STRENGTH": +1},
    built_in_systems=["comm unit", "HUD", "helmet cam", "body cam", "data analysis system", "vitals tracker", "high-beam shoulder lamp"],
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

eco2_high_pressure_suit = SuitItem(
    name="ECO2 All World Systems High Pressure Survival Suit",
    armor_rating=1,
    encumbrance=2.0,
    cost=20000,
    lore="A reinforced EVA suit for vacuum and deep pressure survival with full sensor integration.",
    air_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    hazard_resistances=["high pressure", "vacuum", "extreme cold"],
    built_in_systems=["HUD", "camera", "comm unit", "data ports"],
    zero_g_thrusters=True,
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

yaws3_survival_shelter = SuitItem(
    name="YAWS3 Yutani All Weather Singular Survival Shelter",
    armor_rating=0,
    encumbrance=3.0,
    cost=30000,
    lore="A self-contained survival pod designed for long-term field isolation and emergency containment.",
    air_supply_rating=12,
    power_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    activated_encumbrance=4.0,
    built_in_systems=["PDT", "motion detector", "rebreather", "medkit", "stim delivery system"],
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

el7hxc_hex_capsule = SuitItem(
    name="Omni-Tech EL7-HXC Emergency Landing Hex Capsule",
    armor_rating=1,
    encumbrance=3.0,
    cost=150000,
    lore="An experimental hex-field survival device that deploys a reactive energy shell around its occupant.",
    power_supply_rating=3,
    sealed=False,
    environment_type="limited vacuum",
    activated_encumbrance=4.0,
    special_deflection_dice=10,
    special_deflection_condition="explosive, energy, fire, or radiation damage",
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

armat_cm4_riot_shield = ArmorItem(
    name="Armat CM4 Plastisteel Riot Shield",
    armor_rating=5,
    encumbrance=1.0,
    coverage_slots=["left_arm", "torso"],
    cost=300,
    lore="A lightweight shield used by marines and marshals for cover during urban operations.",
    provides_cover=True
)

military_hazmat_suit = SuitItem(
    name="Military Grade HAZMAT Suit",
    armor_rating=1,
    encumbrance=2.0,
    cost=1000,
    lore="An impermeable bodysuit used in chemically hazardous zones and contaminated facilities.",
    air_supply_rating=2,
    sealed=True,
    environment_type="hazardous",
    hazard_resistances=["chemical", "biological", "radiation"],
    radiation_absorption_dice=6,
    built_in_systems=["comm unit"],
    coverage_slots=["suit", "head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "feet"]
)

udep_environmental_poncho = ClothingItem(
    name="UDEP Ultra Diffusive Environmental Poncho",
    armor_rating=0,
    encumbrance=1.0,
    cost=500,
    lore="A rain-repellent poncho that masks infrared and protects against field exposure to contaminants.",
    conditional_modifiers=[
        {"skill": "STAMINA", "modifier": "+2", "condition": "against chemical and biological contaminants"},
        {"skill": "STEALTH", "modifier": "+2", "condition": "in wet environments"}
    ],
    coverage_slots=["torso"]
)

g_suit = ClothingItem(
    name="G-Suit",
    armor_rating=0,
    encumbrance=1.0,
    cost=120,
    lore="A pilot's jumpsuit with built-in pressure plates and a backup air cylinder.",
    air_supply_rating=1,
    coverage_slots=["torso", "left_leg", "right_leg"]
)

m10_ballistic_helmet = AccessoryItem(
    name="M10 Ballistic Helmet",
    armor_rating=0,
    encumbrance=0,
    slot="head",
    suit_compatible=True,
    cost=0,
    lore="A standard-issue USCMC helmet equipped with tactical optics and IFF targeting.",
    built_in_systems=["tactical camera", "infrared sight", "IFF transmitter"],
    integrated_in="M3 Personnel Armor"
)

life_vest = AccessoryItem(
    name="Life Vest",
    armor_rating=0,
    encumbrance=1.0,
    slot="torso",
    suit_compatible=True,
    cost=65,
    lore="A buoyant inflatable vest designed to keep wearers afloat in most liquids.",
    built_in_systems=["flashlight", "beacon transmitter", "PDT"],
    coverage_slots=["torso"]
)

cold_weather_parka = ClothingItem(
    name="Cold Weather Parka",
    armor_rating=0,
    encumbrance=0.25,
    cost=100,
    lore="A heated hooded coat for extreme cold climates, favored on terraformed worlds.",
    skill_modifiers={"STAMINA": +2},
    coverage_slots=["torso", "left_arm", "right_arm"]
)

# --- Boots ---
m3b_standard_boots = AccessoryItem(
    name="M3B Standard Boots",
    armor_rating=0,
    encumbrance=0,
    slot="feet",
    suit_compatible=True,
    cost=40,
    lore="Common-issue military boots suited for dry decks and base wear."
)

m7_jungle_boots = AccessoryItem(
    name="M7 Jungle Boots",
    armor_rating=0,
    encumbrance=0,
    slot="feet",
    suit_compatible=True,
    cost=60,
    lore="Moisture-wicking footwear designed for prolonged field use in wet zones."
)

m7a_dry_boots = AccessoryItem(
    name="M7A Dry Boots",
    armor_rating=0,
    encumbrance=0,
    slot="feet",
    suit_compatible=True,
    cost=60,
    lore="Moisture-wicking boots designed to prevent foot rot in wet environments."
)

all_wearable_items = [
    bdus,
    ghillie_suit,
    m3_personnel_armor,
    kevlar_riot_vest,
    irc_mk50_compression_suit,
    eco_survival_suit,
    marine_backpack,
    combat_armor_6b90,
    ccc5_compression_suit,
    bimex_personal_shades,
    pdt_locator_set,
    expedition_fatigues,
    m8a2_thermal_boots,
    m11_platypus_fins,
    presidium_mk8_se_suit,
    eco2_high_pressure_suit,
    yaws3_survival_shelter,
    el7hxc_hex_capsule,
    armat_cm4_riot_shield,
    military_hazmat_suit,
    udep_environmental_poncho,
    g_suit,
    m10_ballistic_helmet,
    life_vest,
    cold_weather_parka,
    m3b_standard_boots,
    m7_jungle_boots,
    m7a_dry_boots
]

class WearableLoadout:
    """Represents a character's equipped wearables: clothing, armor, suit, accessories."""
    def __init__(self, clothing: Optional[ClothingItem] = None, armor: Optional[List[ArmorItem]] = None, suit: Optional[SuitItem] = None, accessories: Optional[List[AccessoryItem]] = None):
        self.clothing = clothing
        self.armor = armor if armor is not None else []
        self.suit = suit
        self.accessories = accessories if accessories is not None else []

    def display_loadout(self) -> str:
        lines = ["[LOADOUT]"]
        if self.suit:
            lines.append(f"Suit: {self.suit.name}")
        if self.clothing:
            lines.append(f"Clothing: {self.clothing.name}")
        if self.armor:
            for a in self.armor:
                lines.append(f"Armor: {a.name}")
        if self.accessories:
            for acc in self.accessories:
                lines.append(f"Accessory: {acc.name}")
        if not (self.suit or self.clothing or self.armor or self.accessories):
            lines.append("No wearables equipped.")
        return "\n".join(lines)

    def to_dict(self):
        return {
            'clothing': self.clothing.name if self.clothing else None,
            'armor': [a.name for a in self.armor],
            'suit': self.suit.name if self.suit else None,
            'accessories': [a.name for a in self.accessories],
        }

    @classmethod
    def from_dict(cls, data, all_items=None):
        # all_items: list of all wearable items to match by name
        clothing = None
        armor = []
        suit = None
        accessories = []
        if not all_items:
            from .wearables import all_wearable_items
            all_items = all_wearable_items
        if data.get('clothing'):
            clothing = next((i for i in all_items if i.name == data['clothing']), None)
        if data.get('armor'):
            armor = [next((i for i in all_items if i.name == n), None) for n in data['armor']]
            armor = [a for a in armor if a]
        if data.get('suit'):
            suit = next((i for i in all_items if i.name == data['suit']), None)
        if data.get('accessories'):
            accessories = [next((i for i in all_items if i.name == n), None) for n in data['accessories']]
            accessories = [a for a in accessories if a]
        return cls(clothing=clothing, armor=armor, suit=suit, accessories=accessories) 