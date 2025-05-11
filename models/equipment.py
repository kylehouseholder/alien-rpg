from .equipment_item import EquipmentItem

# === DATA STORAGE ===

long_data_disc = EquipmentItem(
    name="Long-Data Disc",
    cost=30,
    weight=0,
    description="Nano-optical memory disc storing up to 10 zettabytes of data.",
    usage_tags=["data", "storage"]
)

magnetic_tape = EquipmentItem(
    name="Magnetic Tape",
    cost=5,
    weight=0,
    description="Disposable, low-signal storage medium capable of holding 120 terabytes.",
    usage_tags=["data", "storage"]
)

# === DIAGNOSTICS & DISPLAY ===

pr_put_uplink_terminal = EquipmentItem(
    name="PR-PUT Uplink Terminal",
    cost=9000,
    weight=1,
    description="Armored laptop for remotely piloting orbiting ships (COMTECH).",
    skill_modifiers={"COMTECH": 0},
    usage_tags=["diagnostic", "remote_control"]
)

seegson_tape_recorder = EquipmentItem(
    name="Seegson C-Series Tape Recorder",
    cost=75,
    weight=0.5,
    description="Old-tech audio recorder with playback (MANIPULATION +1).",
    skill_modifiers={"MANIPULATION": +1},
    usage_tags=["audio", "recording"]
)

samani_watch = EquipmentItem(
    name="Samani E-Series Watch",
    cost=50,
    weight=0,
    description="Dual-time wristwatch with hull breach sensors (SURVIVAL +1).",
    skill_modifiers={"SURVIVAL": +1},
    slot="wrist",
    usage_tags=["monitoring", "timekeeping"]
)

pdt = EquipmentItem(
    name="Personal Data Transmitter",
    cost=100,
    weight=0,
    description="Tracks vitals and transmits location in hazardous environments.",
    slot="implant",
    usage_tags=["tracking", "monitoring"]
)

iff_transponder = EquipmentItem(
    name="IFF Transponder",
    cost=250,
    weight=0,
    description="Prevents friendly fire from sentry guns when active.",
    slot="implant",
    usage_tags=["identification", "combat"]
)

data_transmitter_card = EquipmentItem(
    name="Data Transmitter Card",
    cost=50,
    weight=0,
    description="Clear plastic plug-in for transferring visual/audio recordings.",
    usage_tags=["data", "transfer"]
)

seegson_pdat = EquipmentItem(
    name="Seegson P-DAT",
    cost=500,
    weight=0.5,
    description="Team coordination tablet with PDT and mapping sync capability.",
    usage_tags=["tactical", "display"]
)

system_diagnostic_device = EquipmentItem(
    name="Seegson System Diagnostic Device",
    cost=300,
    weight=1,
    description="Portable unit to troubleshoot ship systems (COMTECH +2).",
    skill_modifiers={"COMTECH": +2},
    usage_tags=["diagnostic", "technical"]
)

holotab = EquipmentItem(
    name="HoloTab",
    cost=100000,
    weight=None,
    description="Command-grade holographic analysis table (COMMAND +2).",
    skill_modifiers={"COMMAND": +2},
    usage_tags=["tactical", "command"]
)

modular_computing_device = EquipmentItem(
    name="Modular Computing Device",
    cost=8000,
    weight=None,
    description="Portable audiovisual hologram projector for immersive environments.",
    usage_tags=["projection", "data"]
)

# === VISION DEVICES ===

optical_scope = EquipmentItem(
    name="Optical Scope",
    cost=60,
    weight=0,
    description="Precision rifle scope extending effective range by one category.",
    usage_tags=["sight", "combat"]
)

binoculars = EquipmentItem(
    name="Binoculars",
    cost=100,
    weight=0.5,
    description="Visual aid that grants +2 to long-range OBSERVATION rolls.",
    skill_modifiers={"OBSERVATION": +2},
    usage_tags=["scouting", "observation"]
)

m314_tracker = EquipmentItem(
    name="M314 Motion Tracker",
    cost=1200,
    weight=1,
    description="Ultrasonic sensor tracking movement through obstacles. Power Supply 5.",
    power_supply_rating=5,
    requires_power_roll=True,
    sensor_capabilities=["motion"],
    usage_tags=["sensor", "tracking"]
)

m316_tracker = EquipmentItem(
    name="M316 Motion Tracker",
    cost=3000,
    weight=0,
    description="Lightweight version of M314 with reduced range. Power Supply 3.",
    power_supply_rating=3,
    requires_power_roll=True,
    sensor_capabilities=["motion"],
    usage_tags=["sensor", "combat"]
)

head_mounted_sight = EquipmentItem(
    name="Head-Mounted Sight",
    cost=200,
    weight=0.5,
    description="Targeting interface for controlling Sentry Guns and smart weaponry.",
    slot="head",
    usage_tags=["aiming", "combat"]
)

neuro_visor = EquipmentItem(
    name="Neuro Visor",
    cost=10000,
    weight=1,
    description="Monitors and communicates with hypersleeping subjects via COMTECH.",
    skill_modifiers={"COMTECH": 0},
    usage_tags=["medical", "interface"]
)

pups_mapper = EquipmentItem(
    name=""Pups" Mapping Device",
    cost=50000,
    weight=1,
    description="Floating drone that scans terrain and lifeforms one zone per Round.",
    sensor_capabilities=["mapping", "lifeform"],
    usage_tags=["mapping", "survey"]
)

microview_nav = EquipmentItem(
    name="Seegson Microview-2000SE",
    cost=25000,
    weight=None,
    description="Station-integrated navigational tracker—pinpoints user position.",
    usage_tags=["navigation", "station"]
)

# === TOOLS ===

bolt_gun = EquipmentItem(
    name="Watatsumi DV-303 Bolt Gun",
    cost=400,
    weight=1,
    description="High-impact industrial tool. Grants +2 HEAVY MACHINERY.",
    skill_modifiers={"HEAVY MACHINERY": +2},
    usage_tags=["mechanical", "power_tool"]
)

cutting_torch = EquipmentItem(
    name="Cutting Torch",
    cost=300,
    weight=1,
    description="Industrial plasma torch. Grants +2 HEAVY MACHINERY. Power Supply 5.",
    skill_modifiers={"HEAVY MACHINERY": +2},
    power_supply_rating=5,
    requires_power_roll=True,
    usage_tags=["mechanical", "thermal"]
)

maintenance_jack = EquipmentItem(
    name="Maintenance Jack",
    cost=150,
    weight=1,
    description="Heavy mechanical crowbar. Grants +1 HEAVY MACHINERY.",
    skill_modifiers={"HEAVY MACHINERY": +1},
    usage_tags=["mechanical", "utility"]
)

electronic_tools = EquipmentItem(
    name="Electronic Tools",
    cost=250,
    weight=0.5,
    description="Compact kit for circuit diagnostics. Grants +1 COMTECH.",
    skill_modifiers={"COMTECH": +1},
    usage_tags=["technical", "repair"]
)
