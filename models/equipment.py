from .equipment_item import EquipmentItem

# === DATA STORAGE ===

long_data_disc = EquipmentItem(
    name="Long-Data Disc",
    cost=30,
    weight=0.01,  # Very light, portable physical storage medium
    description="Nano-optical memory disc storing up to 10 zettabytes of data.",
    usage_tags=["data", "storage"]
)

magnetic_tape = EquipmentItem(
    name="Magnetic Tape",
    cost=5,
    weight=0.01,  # Disposable and cheap, physically light
    description="Old-style magnetic tape used for stealthy data storage—120 terabytes.",
    usage_tags=["data", "storage"]
)

# === DIAGNOSTICS & DISPLAY ===

computer_terminal = EquipmentItem(
    name="Computer Terminal",
    cost=0,
    weight=None,  # Stationary system
    description="Terminal used to access and process data. Requires COMTECH roll.",
    skill_requirement={"COMTECH": 1},
    usage_tags=["interface", "data"]
)

pr_put_uplink_terminal = EquipmentItem(
    name="PR-PUT Uplink Terminal",
    cost=9000,
    weight=1,
    description="Armored portable terminal for remote spacecraft control.",
    usage_tags=["diagnostic", "remote_control"],
    skill_requirement={"COMTECH": 1}
)

seegson_tape_recorder = EquipmentItem(
    name="Seegson C-Series Tape Recorder",
    cost=75,
    weight=0.5,
    description="Portable audio recorder used to record or play music.",
    skill_modifiers={"MANIPULATION": +1},
    usage_tags=["audio", "recording"]
)

samani_watch = EquipmentItem(
    name="Samani E-Series Watch",
    cost=50,
    weight=0.01,
    description="Wristwatch that tracks time, oxygen, and pressure.",
    skill_modifiers={"SURVIVAL": +1},
    slot="wrist",
    usage_tags=["monitoring", "timekeeping"]
)

pdt = EquipmentItem(
    name="Personal Data Transmitter",
    cost=100,
    weight=0.01,
    description="Tracks user location and vitals.",
    slot="implant",
    usage_tags=["tracking", "monitoring"]
)

iff_transponder = EquipmentItem(
    name="IFF Transponder",
    cost=250,
    weight=0.01,
    description="Prevents automated friendly fire targeting.",
    slot="implant",
    usage_tags=["identification", "combat"]
)

data_transmitter_card = EquipmentItem(
    name="Data Transmitter Card",
    cost=50,
    weight=0.01,
    description="Transfers audiovisual data from suits to terminals.",
    usage_tags=["data", "transfer"]
)

seegson_pdat = EquipmentItem(
    name="Seegson P-DAT",
    cost=500,
    weight=0.5,
    description="Data tablet synced to field team tools like PDTs.",
    usage_tags=["tactical", "display"]
)

system_diagnostic_device = EquipmentItem(
    name="Seegson System Diagnostic Device",
    cost=300,
    weight=1,
    description="Handheld unit for diagnosing mechanical or electronic faults.",
    skill_modifiers={"COMTECH": +2},
    usage_tags=["diagnostic", "technical"]
)

holotab = EquipmentItem(
    name="HoloTab",
    cost=100000,
    weight=None,
    description="Command-grade table projecting holographic tactical maps.",
    skill_modifiers={"COMMAND": +2},
    usage_tags=["tactical", "command"]
)

modular_computing_device = EquipmentItem(
    name="Modular Computing Device",
    cost=8000,
    weight=None,
    description="Advanced immersive hologram projector (6x6m).",
    usage_tags=["projection", "data"]
)

# === VISION DEVICES ===

hi_beam_flashlight = EquipmentItem(
    name="Hi-beam Flashlight",
    cost=45,
    weight=0.5,
    description="Handheld light source that removes darkness penalties in a zone.",
    environmental_effects={"illuminates_zone": True},
    usage_tags=["illumination"]
)

optical_scope = EquipmentItem(
    name="Optical Scope",
    cost=60,
    weight=0.01,
    description="Extends weapon range by one category for aimed shots.",
    usage_tags=["sight", "combat"]
)

binoculars = EquipmentItem(
    name="Binoculars",
    cost=100,
    weight=0.5,
    description="Enhanced vision tool for long-range scouting.",
    skill_modifiers={"OBSERVATION": +2},
    usage_tags=["scouting", "observation"]
)

m314_tracker = EquipmentItem(
    name="M314 Motion Tracker",
    cost=1200,
    weight=1,
    description="Detects motion via ultrasonic waves (LONG range indoors).",
    power_supply_rating=5,
    requires_power_roll=True,
    sensor_capabilities=["motion"],
    usage_tags=["sensor", "tracking"]
)

m316_tracker = EquipmentItem(
    name="M316 Motion Tracker",
    cost=3000,
    weight=0.01,
    description="Compact motion sensor for weapon integration (MEDIUM range indoors).",
    power_supply_rating=3,
    requires_power_roll=True,
    sensor_capabilities=["motion"],
    usage_tags=["sensor", "combat"]
)

head_mounted_sight = EquipmentItem(
    name="Head-Mounted Sight",
    cost=200,
    weight=0.5,
    description="Sight interface for smart gun or sentry targeting.",
    slot="head",
    usage_tags=["aiming", "combat"]
)

neuro_visor = EquipmentItem(
    name="Neuro Visor",
    cost=10000,
    weight=1,
    description="HUD helmet to monitor and interface with hypersleep subjects.",
    skill_requirement={"COMTECH": 1},
    usage_tags=["medical", "interface"]
)

pups_mapper = EquipmentItem(
    name="\"Pups\" Mapping Device",
    cost=50000,
    weight=1,
    description="Drone scanner that maps terrain and detects lifeforms zone-by-zone.",
    sensor_capabilities=["mapping", "lifeform"],
    usage_tags=["mapping", "survey"]
)

microview_nav = EquipmentItem(
    name="Seegson Microview-2000SE",
    cost=25000,
    weight=None,
    description="Station-integrated navigation and tracking display.",
    usage_tags=["navigation", "station"]
)

# === TOOLS ===

bolt_gun = EquipmentItem(
    name="Watatsumi DV-303 Bolt Gun",
    cost=400,
    weight=1,
    description="High-impact industrial fastener tool. Also usable as weapon.",
    skill_modifiers={"HEAVY MACHINERY": +2},
    usage_tags=["mechanical", "power_tool"]
)

cutting_torch = EquipmentItem(
    name="Cutting Torch",
    cost=300,
    weight=1,
    description="Plasma torch for cutting through metal. Requires power after each use.",
    skill_modifiers={"HEAVY MACHINERY": +2},
    power_supply_rating=5,
    requires_power_roll=True,
    usage_tags=["mechanical", "thermal"]
)

maintenance_jack = EquipmentItem(
    name="Maintenance Jack",
    cost=150,
    weight=1,
    description="Industrial lever for opening airlocks and rerouting power.",
    skill_modifiers={"HEAVY MACHINERY": +1},
    usage_tags=["mechanical", "utility"]
)

electronic_tools = EquipmentItem(
    name="Electronic Tools",
    cost=250,
    weight=0.5,
    description="Compact repair kit for electronics and circuit testing.",
    skill_modifiers={"COMTECH": +1},
    usage_tags=["technical", "repair"]
)

# === GENERAL EQUIPMENT ADDITIONS ===

dog_tags = EquipmentItem(
    name="Acrylic Dog Tags",
    cost=50,
    weight=0,
    description="Encoded military ID keys granting access based on rank.",
    usage_tags=["identification", "access"]
)

cbrn_detection_kit = EquipmentItem(
    name="CBRN Detection Kit",
    cost=800,
    weight=1,
    description="Detects radiation, chemical, and biological threats. Grants +2 to Sickness rolls.",
    skill_modifiers={"SICKNESS": +2},
    sensor_capabilities=["radiation", "chemical", "biological"],
    usage_tags=["diagnostic", "hazmat"]
)

marine_pack = EquipmentItem(
    name="Individual Marine Pack",
    cost=100,
    weight=0,
    description="Backpack that expands carrying capacity by 2.",
    capacity_bonus=2,
    usage_tags=["storage", "utility"]
)

tnr_lamp = EquipmentItem(
    name="TNR High Beam Shoulder Lamp",
    cost=60,
    weight=0.5,
    description="Shoulder-mounted or handheld lamp that removes darkness penalties.",
    environmental_effects={"illuminates_zone": True},
    usage_tags=["illumination", "mountable"]
)

muzzle_suppressor = EquipmentItem(
    name="Muzzle Suppressor",
    cost=100,
    weight=0.25,
    description="Suppresses weapon noise; enemies must roll OBSERVATION to detect shots.",
    detection_modifier={"OBSERVATION": -1},
    usage_tags=["stealth", "weapon_addon"]
)

folding_spade = EquipmentItem(
    name="Folding Entrenching Spade",
    cost=30,
    weight=0.5,
    description="Digging tool also usable as a melee weapon (Bonus +1, Damage 2).",
    weapon_properties={"bonus": +1, "damage": 2},
    usage_tags=["digging", "melee"]
)

folding_winch = EquipmentItem(
    name="Folding Winch",
    cost=40,
    weight=1,
    description="Tripod winch with rope. Grants +2 to MOBILITY rolls when climbing.",
    mobility_bonus=2,
    usage_tags=["climbing", "utility"]
)

climbing_rope = EquipmentItem(
    name="Polymer Climbing Rope",
    cost=40,
    weight=0.5,
    description="45-meter abrasion-resistant rope. Not acid-proof.",
    usage_tags=["climbing", "tether"]
)

spotter_scope = EquipmentItem(
    name="F3S Full Spectrum Spotter Scope",
    cost=200,
    weight=0.5,
    description="Assist sniper by providing +1 OBSERVATION per success without movement.",
    skill_modifiers={"OBSERVATION": +1},
    usage_tags=["targeting", "coordination"]
)

m73px_parafoil = EquipmentItem(
    name="M73PX Parafoil",
    cost=1250,
    weight=3,
    description="Collapsible glider used in stealth drops. Speed 3, controlled by PILOTING.",
    skill_modifiers={"PILOTING": +3},
    usage_tags=["aerial", "mobility"]
)

mining_tool_kit = EquipmentItem(
    name="Mining Tool Kit",
    cost=300,
    weight=2,
    description="Heavy-duty tools for mining operations. +2 to HEAVY MACHINERY rolls in mining contexts.",
    skill_modifiers={"HEAVY MACHINERY": +2},
    usage_tags=["mining", "engineering"]
)

lag_attunement_guide = EquipmentItem(
    name="LAG Laser Attunement Guide",
    cost=200,
    weight=0.25,
    description="Adjusts laser beam intensity. Can blind (-1 OBSERVATION) or boost damage (+1, Power Supply roll required).",
    detection_modifier={"OBSERVATION": -1},
    weapon_properties={"damage": +1},
    requires_power_roll=True,
    usage_tags=["laser_module", "targeting"]
)

sddg_fence = EquipmentItem(
    name="Omni-Tech SDDG Sonic Deterrent Defense Grid",
    cost=50000,
    weight=4,
    description="Emits ultrasonic deterrents. Forces STAMINA roll each round in range or suffer +1 STRESS and a Panic Roll.",
    environmental_effects={"sonic_deterrent": True},
    usage_tags=["defense", "perimeter"]
)

heavy_safari_pack = EquipmentItem(
    name="Heavy Safari Pack",
    cost=100,
    weight=0,
    description="Large waterproof backpack with built-in medkit and Supply 6. Increases carrying capacity by 2.",
    capacity_bonus=2,
    usage_tags=["storage", "exploration"]
)
