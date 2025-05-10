from armor_item import ArmorItem

m3_personnel_armor = ArmorItem(
    name="M3 Personnel Armor",
    cost=1200,
    lore="Standard-issue body armor worn by Colonial Marines, known for its rugged, tactical design.",
    armor_rating=6,
    coverage_slots=["torso", "abdomen", "legs"],
    layer=1,
    encumbrance=1.0,
    built_in_systems=["comm unit", "PDT", "vitals monitor", "combat webbing"]
)

irc_mk50_compression_suit = ArmorItem(
    name="IRC Mk.50 Compression Suit",
    cost=15000,
    lore="A dependable, aging vacuum suit still widely used across the Frontier.",
    armor_rating=2,
    air_supply_rating=5,
    sealed=True,
    environment_type="vacuum",
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    encumbrance=1.0,
    built_in_systems=["comm unit", "HUD", "headlamp", "helmet cam"]
)

irc_mk35_pressure_suit = ArmorItem(
    name="IRC Mk.35 Pressure Suit",
    cost=2000,
    lore="A bulky USCMC-issue pressure suit with stiff joints and a dated recycler system.",
    armor_rating=5,
    air_supply_rating=4,
    sealed=True,
    environment_type="vacuum",
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    encumbrance=2.0,
    skill_modifiers={"AGILITY": -1},
    post_use_requirement="requires decompression chamber"
)

eco_survival_suit = ArmorItem(
    name="Eco All-World Survival Suit",
    cost=30000,
    lore="A high-end EVA hardsuit designed for zero-G missions and hostile environments.",
    armor_rating=4,
    air_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    hazard_resistances=["extreme cold", "extreme pressure"],
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    encumbrance=2.0,
    built_in_systems=["HUD", "helmet cam", "comm unit", "data ports"],
    zero_g_thrusters=True
)

weyland_yutani_apesuit = ArmorItem(
    name="Weyland-Yutani APEsuit",
    cost=5000,
    lore="A combat-ready environment suit used in containment and security operations.",
    armor_rating=3,
    air_supply_rating=4,
    sealed=False,
    hazard_resistances=["extreme temperature", "caustic agents"],
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    encumbrance=1.0,
    skill_modifiers={"SURVIVAL": 3},
    built_in_systems=["protective eyewear", "face mask"]
)

p5000_power_loader = ArmorItem(
    name="Caterpillar P-5000 Power Loader",
    cost=50000,
    lore="A mechanized exosuit for heavy lifting and industrial operations.",
    armor_rating=3,
    sealed=False,
    coverage_slots=["torso", "limbs"],
    layer=2,
    encumbrance=None,
    carry_bonus=4,
    built_in_weapon_damage=3,
    required_skills={"HEAVY MACHINERY": 2},
    attribute_modifiers={"STRENGTH": 10}
)

bdus = ArmorItem(
    name="Battledress Utilities (BDUs)",
    cost=55,
    lore="Standard camouflage fatigues worn by troops in all environments.",
    coverage_slots=["torso", "arms", "legs"],
    layer=0,
    encumbrance=0
)

ghillie_suit = ArmorItem(
    name="Ghillie Suit",
    cost=1000,
    lore="Customized camouflage gear designed for stealth in specific terrain.",
    coverage_slots=["torso", "arms", "legs"],
    layer=1,
    encumbrance=1.0,
    conditional_modifiers=[
        {"skill": "MOBILITY", "modifier": "+2", "condition": "when avoiding detection in appropriate terrain"}
    ],
    built_in_systems=["heat masking", "infrared scatter"]
)

m3b_standard_boots = ArmorItem(
    name="M3B Standard Boots",
    cost=40,
    lore="Common-issue military boots suited for dry decks and base wear.",
    coverage_slots=["feet"],
    layer=0,
    encumbrance=0
)

m7_jungle_boots = ArmorItem(
    name="M7 Jungle Boots",
    cost=60,
    lore="Moisture-wicking footwear designed for prolonged field use in wet zones.",
    coverage_slots=["feet"],
    layer=0,
    encumbrance=0
)

m8a2_thermal_boots = ArmorItem(
    name="M8A2 Thermal Boots",
    cost=75,
    lore="Insulated field boots designed to protect against extreme cold.",
    coverage_slots=["feet"],
    layer=0,
    encumbrance=0,
    skill_modifiers={"STAMINA": +1}
)

m11_platypus_fins = ArmorItem(
    name="M11 Performance Enhanced Platypus Fins",
    cost=100,
    lore="Advanced swim fins optimized for rapid underwater movement.",
    coverage_slots=["feet"],
    layer=0,
    encumbrance=0.5,
    conditional_modifiers=[
        {"skill": "MOBILITY", "modifier": "+2", "condition": "when underwater"}
    ]
)

life_vest = ArmorItem(
    name="Life Vest",
    cost=65,
    lore="A buoyant inflatable vest designed to keep wearers afloat in most liquids.",
    encumbrance=1.0,
    coverage_slots=["torso"],
    layer=0,
    built_in_systems=["flashlight", "beacon transmitter", "PDT"]
)

cold_weather_parka = ArmorItem(
    name="Cold Weather Parka",
    cost=100,
    lore="A heated hooded coat for extreme cold climates, favored on terraformed worlds.",
    encumbrance=0.25,
    coverage_slots=["torso", "arms"],
    layer=0,
    skill_modifiers={"STAMINA": +2}
)

military_hazmat_suit = ArmorItem(
    name="Military Grade HAZMAT Suit",
    cost=1000,
    lore="An impermeable bodysuit used in chemically hazardous zones and contaminated facilities.",
    armor_rating=1,
    air_supply_rating=2,
    sealed=True,
    environment_type="hazardous",
    hazard_resistances=["chemical", "biological", "radiation"],
    radiation_absorption_dice=6,
    encumbrance=2.0,
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    built_in_systems=["comm unit"]
)

udep_environmental_poncho = ArmorItem(
    name="UDEP Ultra Diffusive Environmental Poncho",
    cost=500,
    lore="A rain-repellent poncho that masks infrared and protects against field exposure to contaminants.",
    encumbrance=1.0,
    coverage_slots=["torso"],
    layer=1,
    conditional_modifiers=[
        {"skill": "STAMINA", "modifier": "+2", "condition": "against chemical and biological contaminants"},
        {"skill": "STEALTH", "modifier": "+2", "condition": "in wet environments"}
    ]
)

g_suit = ArmorItem(
    name="G-Suit",
    cost=120,
    lore="A pilot’s jumpsuit with built-in pressure plates and a backup air cylinder.",
    air_supply_rating=1,
    encumbrance=1.0,
    coverage_slots=["legs", "torso"],
    layer=0
)

m10_ballistic_helmet = ArmorItem(
    name="M10 Ballistic Helmet",
    cost=0,
    lore="A standard-issue USCMC helmet equipped with tactical optics and IFF targeting.",
    encumbrance=0,
    coverage_slots=["head"],
    layer=1,
    built_in_systems=["tactical camera", "infrared sight", "IFF transmitter"],
    integrated_in="M3 Personnel Armor"
)

kevlar_riot_vest = ArmorItem(
    name="Kevlar Riot Vest",
    cost=600,
    lore="Woven fiber body armor used by colonial law enforcement and security teams.",
    armor_rating=4,
    encumbrance=1.0,
    coverage_slots=["torso"],
    layer=1,
    built_in_systems=["comm unit"]
)

armat_cm4_riot_shield = ArmorItem(
    name="Armat CM4 Plastisteel Riot Shield",
    cost=300,
    lore="A lightweight shield used by marines and marshals for cover during urban operations.",
    armor_rating=5,
    encumbrance=1.0,
    coverage_slots=["arm", "front"],
    layer=1,
    provides_cover=True
)

combat_armor_6b90 = ArmorItem(
    name="6B90 Combat Armor",
    cost=1000,
    lore="Heavier than USCMC gear, this bulky UPP armor protects vital areas with tactical oversight.",
    armor_rating=6,
    encumbrance=2.0,
    coverage_slots=["neck", "shoulders", "torso", "crotch"],
    layer=1,
    built_in_systems=["comm unit", "tactical camera"]
)

ccc5_compression_suit = ArmorItem(
    name="CCC5 Combat Compression Suit",
    cost=15500,
    lore="An armored vacuum suit with a narrow helmet view and a built-in AK-104 rifle.",
    armor_rating=2,
    air_supply_rating=5,
    sealed=True,
    environment_type="vacuum",
    encumbrance=2.0,
    coverage_slots=["torso", "limbs", "head"],
    layer=1,
    skill_modifiers={"OBSERVATION": -1},
    integrated_weapon="AK-104"
)

bimex_personal_shades = ArmorItem(
    name="BiMex Personal Shades",
    cost=150,
    lore="Stylish, military-issue eyewear designed to shield against battlefield glare and optical hazards.",
    encumbrance=0,
    coverage_slots=["eyes"],
    layer=0,
    conditional_deflection={
        "trigger": "hit by laser weapon",
        "mechanic": "Roll 1 Base Die; on 6, beam is deflected and damage is negated; item is destroyed"
    }
)

pdt_locator_set = ArmorItem(
    name="PDT/L Bracelet and Locator Tube",
    cost=100,
    lore="A short-range tracking system pairing a wrist-worn transmitter with a directional locator tube.",
    encumbrance=0.25,
    coverage_slots=["wrist"],
    layer=0,
    locator_linked=True
)

expedition_fatigues = ArmorItem(
    name="Expedition Fatigues",
    cost=55,
    lore="Thermal-regulating undersuit designed for frontier exploration in extreme climates.",
    encumbrance=0,
    coverage_slots=["torso", "arms", "legs"],
    layer=0,
    skill_modifiers={"STAMINA": +1},
    hazard_resistances=["heat", "cold", "vacuum"]
)

m7a_dry_boots = ArmorItem(
    name="M7A Dry Boots",
    cost=60,
    lore="Moisture-wicking boots designed to prevent foot rot in wet environments.",
    encumbrance=0,
    coverage_slots=["feet"],
    layer=0
)

m8a2_thermal_boots = ArmorItem(
    name="M8A2 Thermal Boots",
    cost=75,
    lore="Insulated boots made for prolonged exposure to freezing temperatures.",
    encumbrance=0,
    coverage_slots=["feet"],
    layer=0,
    skill_modifiers={"STAMINA": +1}
)

m11_platypus_fins = ArmorItem(
    name="M11 Performance Enhanced Platypus Fins",
    cost=100,
    lore="Advanced fins engineered for high-performance aquatic movement.",
    encumbrance=0.5,
    coverage_slots=["feet"],
    layer=0,
    conditional_modifiers=[
        {"skill": "MOBILITY", "modifier": "+2", "condition": "when underwater"}
    ]
)

presidium_mk8_se_suit = ArmorItem(
    name="Presidium Mark VIII Advanced SE Suit",
    cost=5000,
    lore="A sleek, reinforced exosuit designed for Weyland-era deep space expeditions.",
    armor_rating=1,
    air_supply_rating=3,
    sealed=True,
    environment_type="vacuum",
    encumbrance=2.0,
    layer=2,
    attribute_modifiers={"STRENGTH": +1},
    built_in_systems=["comm unit", "HUD", "helmet cam", "body cam", "data analysis system", "vitals tracker", "high-beam shoulder lamp"]
)

ccc4_cosmos_compression_suit = ArmorItem(
    name="CCC4 Cosmos Corps Compression Suit",
    cost=600,
    lore="A lightweight vacuum suit with limited tactical utility and minimal protection.",
    armor_rating=0,
    air_supply_rating=3,
    sealed=True,
    environment_type="vacuum",
    encumbrance=1.0,
    layer=1,
    skill_modifiers={"OBSERVATION": -1}
)

eco2_high_pressure_suit = ArmorItem(
    name="ECO2 All World Systems High Pressure Survival Suit",
    cost=20000,
    lore="A reinforced EVA suit for vacuum and deep pressure survival with full sensor integration.",
    armor_rating=1,
    air_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    encumbrance=2.0,
    layer=2,
    hazard_resistances=["high pressure", "vacuum", "extreme cold"],
    built_in_systems=["HUD", "camera", "comm unit", "data ports"],
    zero_g_thrusters=True
)

yaws3_survival_shelter = ArmorItem(
    name="YAWS3 Yutani All Weather Singular Survival Shelter",
    cost=30000,
    lore="A self-contained survival pod designed for long-term field isolation and emergency containment.",
    air_supply_rating=12,
    power_supply_rating=6,
    sealed=True,
    environment_type="vacuum",
    encumbrance=3.0,
    activated_encumbrance=4.0,
    layer=2,
    built_in_systems=["PDT", "motion detector", "rebreather", "medkit", "stim delivery system"]
)

el7hxc_hex_capsule = ArmorItem(
    name="Omni-Tech EL7-HXC Emergency Landing Hex Capsule",
    cost=150000,
    lore="An experimental hex-field survival device that deploys a reactive energy shell around its occupant.",
    armor_rating=1,
    power_supply_rating=3,
    sealed=False,
    environment_type="limited vacuum",
    encumbrance=3.0,
    activated_encumbrance=4.0,
    layer=2,
    special_deflection_dice=10,
    special_deflection_condition="explosive, energy, fire, or radiation damage"
)

# --- ALL ARMOR ITEMS ---

all_armor_items = [
    m3_personnel_armor,
    irc_mk50_compression_suit,
    irc_mk35_pressure_suit,
    eco_survival_suit,
    weyland_yutani_apesuit,
    p5000_power_loader,
    bdus,
    ghillie_suit,
    m3b_standard_boots,
    m7_jungle_boots,
    m8a2_thermal_boots,
    m11_platypus_fins,
    life_vest,
    cold_weather_parka,
    military_hazmat_suit,
    udep_environmental_poncho,
    g_suit,
    m10_ballistic_helmet,
    kevlar_riot_vest,
    armat_cm4_riot_shield,
    combat_armor_6b90,
    ccc5_compression_suit,
    bimex_personal_shades,
    pdt_locator_set,
    expedition_fatigues,
    m7a_dry_boots,
    presidium_mk8_se_suit,
    ccc4_cosmos_compression_suit,
    eco2_high_pressure_suit,
    yaws3_survival_shelter,
    el7hxc_hex_capsule,
]
