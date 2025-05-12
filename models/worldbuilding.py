import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import os
import json
import math

# Constants for gravity calculations
G = 6.67430e-11  # Gravitational constant in m³/kg/s²
EARTH_MASS = 5.972e24  # Earth's mass in kg
EARTH_RADIUS = 6371000  # Earth's radius in meters
EARTH_GRAVITY = 9.81  # Earth's surface gravity in m/s²
DEFAULT_DENSITY = 4500  # Default density in kg/m³ (4.5 g/cm³) - average of terrestrial planets

def calculate_surface_gravity(diameter_km: float, density_kg_m3: float = DEFAULT_DENSITY) -> float:
    """
    Calculate surface gravity for a body using the formula g = (4/3) * π * G * ρ * r
    Returns gravity in Earth g units (1.0 = Earth gravity)
    """
    # Convert diameter to radius in meters
    radius_m = (diameter_km * 1000) / 2
    
    # Calculate mass using volume and density
    volume = (4/3) * math.pi * radius_m**3
    mass = volume * density_kg_m3
    
    # Calculate surface gravity in m/s²
    gravity_ms2 = (G * mass) / (radius_m**2)
    
    # Convert to Earth g units
    gravity_g = gravity_ms2 / EARTH_GRAVITY
    
    # Ensure we never return exactly zero and round to nearest 0.01g
    return round(max(gravity_g, 1e-5), 2)  # Minimum gravity of 0.01g, rounded to 2 decimal places

# ===========================================================================
# STARS: Definitions & Generation Utilities
# ===========================================================================

class StarType(Enum):
    """
    Primary categories of stars used in the system.
    Affects planet-roll modifiers and narrative descriptors.
    """
    GIANT = "Giant"
    SUBGIANT = "Subgiant"
    MAIN_SEQUENCE = "Main Sequence"
    WHITE_DWARF = "White Dwarf"
    RED_DWARF = "Red Dwarf"
    WHITE_MAIN_SEQUENCE = "White Main Sequence"

class BrightnessClass(Enum):
    """Brightness classification codes tied to each star type."""
    III = "III"        # Giants
    IV = "IV"          # Subgiants
    V = "V"            # Main Sequence
    DA = "DA"          # White Dwarfs
    MV = "MV"          # Red Dwarfs
    A0V = "A0V"        # White Main Sequence

class SpectralClass(Enum):
    """Spectral temperature classes (O–M)."""
    O = "O"
    B = "B"
    A = "A"
    F = "F"
    G = "G"
    K = "K"
    M = "M"

@dataclass
class Star:
    """
    Represents a star instance with a name and classification.
    """
    name: str
    star_type: StarType
    brightness_class: BrightnessClass
    spectral_class: Optional[SpectralClass] = None

@dataclass
class StarTypeProperties:
    """
    Holds generation modifiers and narrative notes for each StarType.
    - habitable_zone: inner/outer bounds (AU)
    - typical_lifetime_gyr: lifespan in billions of years
    - gas_giant_modifier: adjustment to 1d6+1 gas giant rolls
    - terrestrial_modifier: adjustment to 1d6 terrestrial rolls
    - ice_modifier: adjustment to 1d6+1 ice planet rolls
    - belt_modifier: adjustment to 1d6-3 asteroid belts
    - spectral_influence: descriptive lore/hazards
    """
    habitable_zone: Tuple[float, float]
    typical_lifetime_gyr: float
    gas_giant_modifier: int
    terrestrial_modifier: int
    ice_modifier: int
    belt_modifier: int
    spectral_influence: str

# Mapping each StarType to its corresponding modifiers and lore.
star_type_properties_path = os.path.join(os.path.dirname(__file__), '../data/star_type_properties.json')
with open(star_type_properties_path, 'r') as f:
    _star_type_properties_json = json.load(f)
STAR_TYPE_PROPERTIES: Dict[StarType, StarTypeProperties] = {
    StarType[key]: StarTypeProperties(
        tuple(value["habitable_zone"]),
        value["typical_lifetime_gyr"],
        value["gas_giant_modifier"],
        value["terrestrial_modifier"],
        value["ice_modifier"],
        value["belt_modifier"],
        value["spectral_influence"]
    )
    for key, value in _star_type_properties_json.items()
}

# ---------------------------------------------------------------------------
# Star Name Generation
# ---------------------------------------------------------------------------
# Pools for different naming conventions:
GREEK_LETTERS = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
CATALOG_PREFIXES = ['HR','HD','Gliese']
SECTOR_LETTERS = [chr(c) for c in range(ord('A'),ord('Z')+1)]
SECTOR_DIGITS = list(range(1,10))
ALPHANUM_PREFIXES = ['SYS','XQ','ZT']


def generate_star_name(style: Optional[int] = None) -> str:
    """
    Create a star name using one of four styles:
      1) Catalog + Greek letter + number
      2) Sector-grid code (e.g. A5-3B)
      3) Alphanumeric serial (e.g. SYS-123)
      4) Random hybrid of the above
    If no style is specified, choose one at random.
    """
    if style is None:
        style = random.choice([1,2,3,4])
    def s1() -> str:
        """Generate a star name in the format: Catalog + Greek letter + number."""
        return f"{random.choice(CATALOG_PREFIXES)} {random.choice(GREEK_LETTERS)}-{random.randint(1,20)}"
    def s2() -> str:
        """Generate a star name in the format: Sector-grid code (e.g. A5-3B)."""
        return f"{random.choice(SECTOR_LETTERS)}{random.choice(SECTOR_DIGITS)}-{random.choice(SECTOR_DIGITS)}{random.choice(SECTOR_LETTERS)}"
    def s3() -> str:
        """Generate a star name in the format: Alphanumeric serial (e.g. SYS-123)."""
        return f"{random.choice(ALPHANUM_PREFIXES)}-{random.randint(100,999)}"
    def s4() -> str:
        """Generate a star name using a random hybrid of the above styles."""
        return random.choice([s1(), s2(), s3()])
    return {1:s1, 2:s2, 3:s3, 4:s4}.get(style, s1)()

# ===========================================================================
# PLANETS: Types, Naming & Features
# ===========================================================================

class PlanetType(Enum):
    """Categories of planetary bodies."""
    TERRESTRIAL = 'Terrestrial'
    GAS_GIANT = 'Gas Giant'
    ICE = 'Ice'
    ASTEROID_BELT = 'Asteroid Belt'

def get_gas_giant_moon_count() -> int:
    """
    Gas giants inherently host a sizable satellite system: roll 1d6 and add 4
    to determine the number of significant moons (regardless of orbit table).
    """
    return random.randint(1, 6) + 4

# Name pools for colonized worlds vs unsurveyed bodies.
INHABITED_PLANET_NAMES = [
    'Hannibal','Monos','Requiem','Nakaya','Phaeton','Nocturne','Prospero',
    'Magdala','Hamilton','Tracatus','Aurora','Arges','Damnation','Nero',
    'Doramin','Solitude','Euphrates','Nemesis','Moab','Steropes','Napier'
]
PLANET_PREFIX_MAP: Dict[PlanetType, List[str]] = {
    PlanetType.TERRESTRIAL: ['LV','MT','RF','AX','QX','KH','TR','YE','GN','MP'],
    PlanetType.GAS_GIANT:   ['GG','JB','CD','VX','PR','HY','MN','SR','DK','TP'],
    PlanetType.ICE:         ['IC','NF','GL','BR','ZX','NL','FJ','SY','WV','PL'],
    PlanetType.ASTEROID_BELT:['AS','CB','RB','AB','ST','KT','XR','VL','NP','DJ'],
}

def generate_planet_name(planet_type: PlanetType, colonized: bool=False) -> str:
    """
    Return a mythological name (50% chance if colonized) or
    a type-specific prefix code for unsurveyed planets.
    """
    if colonized and random.random() < 0.5:
        return random.choice(INHABITED_PLANET_NAMES)
    prefix = random.choice(PLANET_PREFIX_MAP[planet_type])
    return f"{prefix}-{random.randint(1,999):03d}"

# ===========================================================================
# PLANET SIZE: Categories based on 2d6 roll
# ===========================================================================

@dataclass
class PlanetSizeCategory:
    """
    Defines a size bracket:
    - roll_min/roll_max: 2d6 range
    - diameter_km: physical size
    - gravity_g: relative surface gravity
    - examples: solar system analogs
    """
    roll_min: int
    roll_max: int
    diameter_km: int
    gravity_g: float
    examples: List[str]

planet_size_categories_path = os.path.join(os.path.dirname(__file__), '../data/planet_size_categories.json')
with open(planet_size_categories_path, 'r') as f:
    _planet_size_categories_json = json.load(f)
PLANET_SIZE_CATEGORIES: List[PlanetSizeCategory] = [
    PlanetSizeCategory(
        entry["roll_min"],
        entry["roll_max"],
        entry["diameter_km"],
        entry["gravity_g"],
        entry["examples"]
    )
    for entry in _planet_size_categories_json
]

def get_planet_size_category(roll: int) -> PlanetSizeCategory:
    """
    Return the size category matching a 2d6 roll, with some randomization within the category.
    """
    for cat in PLANET_SIZE_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            # Add some randomization to the diameter (±20%)
            base_diameter = cat.diameter_km
            min_diameter = int(base_diameter * 0.8)
            max_diameter = int(base_diameter * 1.2)
            diameter = random.randint(min_diameter, max_diameter)
            
            # Calculate gravity using scientific formula
            # Use higher density for larger planets (more iron content)
            if diameter > 12000:
                density = 5500  # 5.5 g/cm³ for larger planets (similar to Earth)
            elif diameter > 8000:
                density = 5000  # 5.0 g/cm³ for medium planets
            else:
                density = 4500  # 4.5 g/cm³ for smaller planets
            
            gravity = calculate_surface_gravity(diameter, density_kg_m3=density)
            
            return PlanetSizeCategory(
                roll_min=cat.roll_min,
                roll_max=cat.roll_max,
                diameter_km=diameter,
                gravity_g=gravity,
                examples=cat.examples
            )
    return PLANET_SIZE_CATEGORIES[0]  # fallback to smallest

# ===========================================================================
# ATMOSPHERE GENERATION: 2d6 with diameter-based modifiers
# ===========================================================================

class AtmosphereType(Enum):
    """Possible planet atmospheres."""
    THIN = 'Thin'
    BREATHABLE = 'Breathable'
    TOXIC = 'Toxic'
    DENSE = 'Dense'
    CORROSIVE = 'Corrosive'
    INFILTRATING = 'Infiltrating'
    SPECIAL = 'Special'

@dataclass
class AtmosphereCategory:
    """Roll range and diameter modifier for atmosphere determination."""
    roll_min: int
    roll_max: int
    type: AtmosphereType
    diameter_modifier: int

# Lookup table: apply diameter modifier before category lookup
atmosphere_categories_path = os.path.join(os.path.dirname(__file__), '../data/atmosphere_categories.json')
with open(atmosphere_categories_path, 'r') as f:
    _atmosphere_categories_json = json.load(f)
ATMOSPHERE_CATEGORIES: List[AtmosphereCategory] = [
    AtmosphereCategory(
        entry["roll_min"],
        entry["roll_max"],
        AtmosphereType[entry["type"]],
        entry["diameter_modifier"]
    )
    for entry in _atmosphere_categories_json
]

def get_atmosphere_type(roll: int, diameter_km: int) -> AtmosphereType:
    """
    Adjust roll by diameter penalties, clamp to 2-12, and lookup.
    """
    if diameter_km <= 4000:
        roll -= 6  # small worlds struggle to hold atmosphere
    elif diameter_km <= 7000:
        roll -= 2
    roll = max(2, min(12, roll))
    for cat in ATMOSPHERE_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            return cat.type
    return AtmosphereType.SPECIAL

# ===========================================================================
# TEMPERATURE GENERATION: 2d6 with atmosphere-based modifiers
# ===========================================================================

class TemperatureType(Enum):
    FROZEN = 'Frozen'
    COLD = 'Cold'
    TEMPERATE = 'Temperate'
    HOT = 'Hot'
    BURNING = 'Burning'

@dataclass
class TemperatureCategory:
    roll_min: int
    roll_max: int
    type: TemperatureType

# Base roll categories
temperature_categories_path = os.path.join(os.path.dirname(__file__), '../data/temperature_categories.json')
with open(temperature_categories_path, 'r') as f:
    _temperature_categories_json = json.load(f)
TEMPERATURE_CATEGORIES: List[TemperatureCategory] = [
    TemperatureCategory(
        entry["roll_min"],
        entry["roll_max"],
        TemperatureType[entry["type"]]
    )
    for entry in _temperature_categories_json
]

def get_temperature_type(roll: int, atmosphere: AtmosphereType) -> TemperatureType:
    """
    Modify roll by atmosphere traits, clamp, and lookup temperature.
    """
    if atmosphere == AtmosphereType.THIN:
        roll -= 4
    elif atmosphere == AtmosphereType.DENSE:
        roll += 1
    elif atmosphere in (AtmosphereType.CORROSIVE, AtmosphereType.INFILTRATING):
        roll += 6
    roll = max(2, min(12, roll))
    for cat in TEMPERATURE_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            return cat.type
    return TemperatureType.TEMPERATE

# ===========================================================================
# GEOSPHERE GENERATION: Land/Ocean proportions with modifiers
# ===========================================================================

class GeosphereType(Enum):
    DESERT = 'Desert World'
    ARID = 'Arid World'
    TEMPERATE_DRY = 'Temperate-Dry World'
    TEMPERATE_WET = 'Temperate-Wet World'
    WET = 'Wet World'
    WATER = 'Water World'

@dataclass
class GeosphereCategory:
    roll_min: int
    roll_max: int
    type: GeosphereType
    description: str

# Lookup table with atmosphere+temperature adjustments
geosphere_categories_path = os.path.join(os.path.dirname(__file__), '../data/geosphere_categories.json')
with open(geosphere_categories_path, 'r') as f:
    _geosphere_categories_json = json.load(f)
GEOSPHERE_CATEGORIES: List[GeosphereCategory] = [
    GeosphereCategory(
        entry["roll_min"],
        entry["roll_max"],
        GeosphereType[entry["type"]],
        entry["description"]
    )
    for entry in _geosphere_categories_json
]

def get_geosphere_type(roll: int, atmosphere: AtmosphereType, temperature: TemperatureType) -> GeosphereType:
    """
    Apply atmosphere & temperature penalties, clamp, and lookup geosphere.
    """
    if atmosphere in (AtmosphereType.THIN, AtmosphereType.DENSE,
                       AtmosphereType.CORROSIVE, AtmosphereType.INFILTRATING):
        roll -= 4
    if temperature == TemperatureType.HOT:
        roll -= 2
    elif temperature == TemperatureType.BURNING:
        roll -= 4
    elif temperature == TemperatureType.FROZEN:
        roll -= 2
    roll = max(2, min(12, roll))
    for cat in GEOSPHERE_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            return cat.type
    return GeosphereType.DESERT

# ===========================================================================
# PLANETARY TERRAIN (Terrestrial): D66 table with world modifiers
# ===========================================================================

class TerrainType(Enum):
    """Distinctive terrain features for worlds."""
    HUGE_CRATER           = "Huge impact crater"
    SILICON_PLAINS        = "Plains of silicon glass"
    WIND_CUT_ROCKS        = "Disturbing wind-cut rock formations"
    GLOBAL_DUST_STORM     = "Permanent global dust-storm"
    EARLY_DUST_PLAINS     = "Eerily colored dust plains"
    ACTIVE_LAVA_FIELDS    = "Active volcanic lava fields"
    EXTENSIVE_SALT_FLATS  = "Extensive salt flats"
    DUSTY_SUNSET_SKY      = "Dust-laden, permanent sunset sky"
    BLACKENED_LAVA        = "Ancient, blackened lava plains"
    THERMAL_SPRINGS       = "Thermal springs and steam vents"
    GRAVELY_MOUNTAINS     = "Tall, gravel-strewn mountains"
    HOWLING_WINDS         = "Howling winds that never stop"
    DAILY_FOG_BANKS       = "Daily fog banks roll in"
    DEEP_RIFT_VALLEYS     = "Deep and wide rift valleys"
    BADLANDS              = "Bizarrely eroded, wind-cut badlands"
    STEEP_RIVER_GORGES    = "Steep-sided river gorges cut into soft rocks"
    HUGE_MOON_DOMINION    = "Huge moon dominates day/night sky"
    WORLD_SPANNING_CANYON = "World-spanning super canyon"
    IMPRESSIVE_RIVER      = "Impressive river of great length"
    ALIEN_FOREST          = "Oddly colored forests of alien vegetation"
    MOUNTAINS_SKYLIGHT    = "Mountains cut by sky-blue lakes"
    ELEPHANT_GRASS        = "Sweeping plains of elephant grass"
    TOXIC_LIFE            = "Highly toxic, but beautiful, plant-life"
    ORBITAL_HABITAT       = "Small, bright, incredibly fast moons in orbit"
    RIVER_DELTA           = "Vast and complex river delta"
    IMMENSE_WATERFALLS    = "Immense series of waterfalls"
    TWISTING_WATERWAYS    = "Endless multitudes with twisting waterways"
    FJORDS_AND_CLIFFS     = "Impressive coastline of fjords and cliffs"
    VOLCANOES_ACTIVE      = "Volcanoes, active & widespread"
    JUNGLE_IMPENETRABLE   = "Impenetrable jungle"
    SURFACE_STORMS        = "Dangerous tides—fast and loud"
    SUPER_STORM           = "Vast, permanent super storm"
    TOXIC_SEA_CREATURES   = "Toxic sea creatures floating with the currents"
    VOLCANIC_ISLANDS      = "Volcanic island chains"
    PERMA_RAINFALL        = "Permanently overcast with unrelenting rainfall"
    OCEANIC_RAIN          = "Mildly acidic oceans and rainfall"

@dataclass
class TerrainCategory:
    """
    D66 roll range and modifier for terrain determination.
    world_modifier adjusts the tens digit (e.g. Desert:-3, Wet:+2).
    """
    roll_min: int
    roll_max: int
    terrain: TerrainType
    world_modifier: int

# Complete map of D66 outcomes (2–66)
terrain_categories_path = os.path.join(os.path.dirname(__file__), '../data/terrain_categories.json')
with open(terrain_categories_path, 'r') as f:
    _terrain_categories_json = json.load(f)
TERRAIN_CATEGORIES: List[TerrainCategory] = [
    TerrainCategory(
        entry["roll_min"],
        entry["roll_max"],
        TerrainType[entry["terrain"]],
        entry["world_modifier"]
    )
    for entry in _terrain_categories_json
]

def get_planetary_terrain(roll: int, world_modifier: int = 0) -> TerrainType:
    """
    Apply world_modifier (tens digit adjustment), clamp to 2–66,
    then return the corresponding TerrainType from the D66 table.
    """
    r = max(2, min(66, roll + world_modifier))
    for cat in TERRAIN_CATEGORIES:
        if cat.roll_min <= r <= cat.roll_max:
            return cat.terrain
    return TerrainType.SILICON_PLAINS

# ===========================================================================
# Ice-Planet Terrain Table
# ===========================================================================
ice_terrain_features_path = os.path.join(os.path.dirname(__file__), '../data/ice_terrain_features.json')
with open(ice_terrain_features_path, 'r') as f:
    _ice_terrain_features_json = json.load(f)
ICE_TERRAIN_FEATURES: Dict[int, str] = {int(k): v for k, v in _ice_terrain_features_json.items()}

def get_ice_planet_terrain(roll: int) -> str:
    """
    Return an ice-planet terrain feature based on a raw 2d6 roll.
    """
    return ICE_TERRAIN_FEATURES.get(roll, ICE_TERRAIN_FEATURES[2])

# EOF: Worldbuilding module with detailed comments and tables

# ---------------------------------------------------------------------------
# COLONY GENERATION: Colony Size, Missions, Orbits, Factions, Allegiance
# ---------------------------------------------------------------------------

class ColonySize(Enum):
    START_UP = 'Start-Up'
    YOUNG = 'Young'
    ESTABLISHED = 'Established'

@dataclass
class ColonySizeCategory:
    roll_min: int
    roll_max: int
    size: ColonySize
    population_formula: str  # e.g. '3d6 x 10'
    base_missions: str       # e.g. '1', 'D3-1', 'D3'

colony_size_categories_path = os.path.join(os.path.dirname(__file__), '../data/colony_size_categories.json')
with open(colony_size_categories_path, 'r') as f:
    _colony_size_categories_json = json.load(f)
COLONY_SIZE_CATEGORIES: List[ColonySizeCategory] = [
    ColonySizeCategory(
        entry["roll_min"],
        entry["roll_max"],
        ColonySize[entry["size"]],
        entry["population_formula"],
        entry["base_missions"]
    )
    for entry in _colony_size_categories_json
]

def get_colony_size(roll: int, atmosphere: AtmosphereType, diameter_km: int) -> ColonySizeCategory:
    """
    Determine colony size by 2d6 roll with modifiers:
      +1 Breathable, -2 Corrosive/Infiltrating, -3 Size<=4000km
    """
    if atmosphere == AtmosphereType.BREATHABLE:
        roll += 1
    elif atmosphere in (AtmosphereType.CORROSIVE, AtmosphereType.INFILTRATING):
        roll -= 2
    if diameter_km <= 4000:
        roll -= 3
    roll = max(2, min(12, roll))
    for cat in COLONY_SIZE_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            return cat
    return COLONY_SIZE_CATEGORIES[0]

class ColonyMissionType(Enum):
    TERRAFORMING     = 'Terraforming'
    RESEARCH         = 'Research'
    SURVEY_PROSPECT  = 'Survey & Prospecting'
    PRISON           = 'Prison/Secluded/Exile'
    MINING_REFINING  = 'Mining & Refining'
    MINERAL_DRILLING = 'Mineral Drilling'
    COMMS_RELAY      = 'Communications Relay'
    MILITARY         = 'Military'
    CATTLE_LOGGING   = 'Cattle Ranching/Logging'
    CORPORATE_HQ     = 'Corporate HQ'
    GOVT_HQ          = 'Government HQ'

colony_mission_table_path = os.path.join(os.path.dirname(__file__), '../data/colony_mission_table.json')
with open(colony_mission_table_path, 'r') as f:
    _colony_mission_table_json = json.load(f)
COLONY_MISSION_TABLE: Dict[int, ColonyMissionType] = {int(k): ColonyMissionType[v] for k, v in _colony_mission_table_json.items()}

def get_colony_mission(roll: int, colony_size: ColonySize, atmosphere: AtmosphereType) -> ColonyMissionType:
    """
    Determine colony mission by 2d6 roll with modifiers:
      Start-Up: -1, Established: +4, Breathable: +1, Corrosive/Infiltrating: -6
    """
    if colony_size == ColonySize.START_UP:
        roll -= 1
    elif colony_size == ColonySize.ESTABLISHED:
        roll += 4
    if atmosphere == AtmosphereType.BREATHABLE:
        roll += 1
    elif atmosphere in (AtmosphereType.CORROSIVE, AtmosphereType.INFILTRATING):
        roll -= 6
    roll = max(2, min(12, roll))
    return COLONY_MISSION_TABLE[roll]

class OrbitType(Enum):
    NONE              = 'None or wreckage'
    RING              = 'Ring'
    SATELLITE_STATION = 'Abandoned/repurposed station'
    MOONS             = 'Moons (roll D3)'
    SURVEY_SATS       = 'Survey & comms satellites'
    TRANSFER_STATION  = 'Transfer station'
    MULTIPLE_MOONS    = 'Multiple objects (roll D6)'

@dataclass
class OrbitCategory:
    roll_min: int
    roll_max: int
    type: OrbitType
    young_modifier: int
    established_modifier: int

orbit_categories_path = os.path.join(os.path.dirname(__file__), '../data/orbit_categories.json')
with open(orbit_categories_path, 'r') as f:
    _orbit_categories_json = json.load(f)
ORBIT_CATEGORIES: List[OrbitCategory] = [
    OrbitCategory(
        entry["roll_min"],
        entry["roll_max"],
        OrbitType[entry["type"]],
        entry["young_modifier"],
        entry["established_modifier"]
    )
    for entry in _orbit_categories_json
]

def get_orbit_components(roll: int, colony_size: ColonySize) -> OrbitType:
    """
    Determine orbital objects by 2d6 roll with colony modifiers:
      Young: +1, Established: +2
    """
    if colony_size == ColonySize.YOUNG:
        roll += 1
    elif colony_size == ColonySize.ESTABLISHED:
        roll += 2
    roll = max(2, min(12, roll))
    for cat in ORBIT_CATEGORIES:
        if cat.roll_min <= roll <= cat.roll_max:
            return cat.type
    return OrbitType.NONE

# ---------------------------------------------------------------------------
# Factions
# ---------------------------------------------------------------------------

def get_num_factions(roll: int) -> int:
    """
    Determine the number of factions by D6 roll.
    Returns the roll if less than 6, otherwise rolls 1d6.
    """
    return roll if roll < 6 else random.randint(1,6)

class FactionType(Enum):
    NEWCOMERS = 'Newcomers'
    CORPORATE_REP = 'Corporate Representatives'
    SCIENTISTS = 'Scientists'
    WORKERS = 'Workers'
    MILITARY = 'Security/Military'
    LEADERSHIP = 'Colonial Leadership'


def get_colony_factions(count: int) -> List[FactionType]:
    """
    Return a list of unique factions present at the colony.
    The number of factions returned is the minimum of count and the number of available FactionTypes.
    """
    return random.sample(list(FactionType), k=min(count, len(FactionType)))

# ---------------------------------------------------------------------------
# Colony Allegiance
# ---------------------------------------------------------------------------
class ColonyAllegiance(Enum):
    UPP = 'Independent Core System Colonies'
    KELLAND = 'Kelland Mining'
    GEOFUND = 'GeoFund Investor'
    GUSTAFSSON = 'Gustafsson Enterprise'
    SEEGSON = 'Seegson'
    NONE = 'No allegiance (Independent)'
    JINGTI = 'Jingti Long Corporation'
    CHIGUSA = 'Chigusa Corporation'
    LASALLE = 'Lasalle Bionational'
    WEYLAND = 'Weyland-Yutani'
    LORENZ = 'Lorenz SysTech'
    GEMINI = 'Gemini Exoplanet'
    FARSIDE = 'Farside Mining'

colony_allegiance_table_path = os.path.join(os.path.dirname(__file__), '../data/colony_allegiance_table.json')
with open(colony_allegiance_table_path, 'r') as f:
    _colony_allegiance_table_json = json.load(f)
COLONY_ALLEGIANCE_TABLE: Dict[int, ColonyAllegiance] = {int(k): ColonyAllegiance[v] for k, v in _colony_allegiance_table_json.items()}

def get_colony_allegiance(roll: int) -> ColonyAllegiance:
    """Lookup colony allegiance by a 3d6 roll (UPP domain)."""
    return COLONY_ALLEGIANCE_TABLE.get(roll, ColonyAllegiance.NONE)

# EOF: Worldbuilding module with updated colony generation

class ExplorationStatus(Enum):
    """Possible exploration states for orbital bodies."""
    UNDISCOVERED = "Undiscovered"  # Not even detected by ICC
    DETECTED = "Detected"          # Known to exist but unexplored
    SURVEYED = "Surveyed"          # Basic survey completed
    EXPLORED = "Explored"          # Detailed exploration completed
    COLONIZED = "Colonized"        # Has a colony

@dataclass
class OrbitalBody:
    """Represents any orbital body with exploration status."""
    name: str
    type: PlanetType
    exploration_status: ExplorationStatus
    distance_au: float
    parent_star: str  # Name of the parent star

def generate_orbital_body_name(star_name: str, body_type: PlanetType, distance_au: float, 
                             exploration_status: ExplorationStatus) -> str:
    """
    Generate a name for an orbital body based on its star and exploration status.
    """
    if exploration_status == ExplorationStatus.UNDISCOVERED:
        return "Undiscovered Body"
    
    # Extract the prefix from the star name (e.g., "HR" from "HR ω-9")
    star_prefix = star_name.split()[0]
    
    # For detected but unexplored bodies
    if exploration_status == ExplorationStatus.DETECTED:
        return f"{star_prefix}-{distance_au:.1f}AU"
    
    # For surveyed/explored/colonized bodies
    if exploration_status == ExplorationStatus.COLONIZED and random.random() < 0.5:
        return random.choice(INHABITED_PLANET_NAMES)
    
    # Generate a type-specific code
    prefix = random.choice(PLANET_PREFIX_MAP[body_type])
    return f"{star_prefix}-{prefix}-{random.randint(1,999):03d}"

def determine_exploration_status(roll: int, has_colony: bool = False) -> ExplorationStatus:
    """
    Determine exploration status based on a 2d6 roll.
    """
    if has_colony:
        return ExplorationStatus.COLONIZED
    
    if roll <= 3:
        return ExplorationStatus.UNDISCOVERED
    elif roll <= 6:
        return ExplorationStatus.DETECTED
    elif roll <= 9:
        return ExplorationStatus.SURVEYED
    else:
        return ExplorationStatus.EXPLORED

def get_moon_size_category(parent_diameter_km: int) -> PlanetSizeCategory:
    """
    Generate a size category for a moon that is appropriately smaller than its parent body.
    The moon's diameter will be between 2-12% of the parent's diameter.
    There's also a chance (25%) of a "super moon" that's 12-25% of the parent's diameter.
    """
    # Roll for super moon chance (25% chance, increased from 20%)
    is_super_moon = random.random() < 0.25
    
    if is_super_moon:
        # Super moon: 12-25% of parent diameter (increased from 10-20%)
        min_diameter = int(parent_diameter_km * 0.12)
        max_diameter = int(parent_diameter_km * 0.25)
    else:
        # Normal moon: 2-12% of parent diameter (increased from 2-10%)
        min_diameter = int(parent_diameter_km * 0.02)
        max_diameter = int(parent_diameter_km * 0.12)
    
    # Generate a random diameter within the range
    moon_diameter = random.randint(min_diameter, max_diameter)
    
    # Determine if the moon is likely to be rocky or icy
    # Moons closer to their parent (smaller diameter) are more likely to be rocky
    is_rocky = random.random() < (1 - (moon_diameter / max_diameter))
    
    # Use different densities for rocky vs icy moons
    if is_rocky:
        # Rocky moon density (similar to terrestrial planets)
        # Use higher density for larger rocky moons
        if moon_diameter > 15000:
            density = 5500  # 5.5 g/cm³ for larger rocky moons (similar to Earth)
        elif moon_diameter > 10000:
            density = 5000  # 5.0 g/cm³ for medium rocky moons
        else:
            density = 4500  # 4.5 g/cm³ for smaller rocky moons
    else:
        # Icy moon density (similar to outer solar system moons)
        if moon_diameter > 15000:
            density = 2500  # 2.5 g/cm³ for larger icy moons
        else:
            density = 2000  # 2.0 g/cm³ for smaller icy moons
    
    # Calculate gravity using scientific formula with appropriate density
    gravity = calculate_surface_gravity(moon_diameter, density_kg_m3=density)
    
    return PlanetSizeCategory(
        roll_min=2,
        roll_max=12,
        diameter_km=moon_diameter,
        gravity_g=gravity,
        examples=["Gas Giant Moon"]
    )

def get_dwarf_planet_size() -> PlanetSizeCategory:
    """
    Generate a size category for a dwarf planet in an asteroid belt.
    Dwarf planets are small, between 500-2000km diameter.
    """
    diameter = random.randint(500, 2000)
    # Calculate gravity using scientific formula
    gravity = calculate_surface_gravity(diameter)
    
    return PlanetSizeCategory(
        roll_min=2,
        roll_max=12,
        diameter_km=diameter,
        gravity_g=gravity,  # Already rounded in calculate_surface_gravity
        examples=["Dwarf Planet"]
    )

def get_gas_giant_size() -> PlanetSizeCategory:
    """
    Generate a size category for a gas giant.
    Gas giants are large, between 50,000-400,000km diameter.
    Uses a lower density for gas giants (1.3 g/cm³)
    """
    # Increased max size to 400,000km to allow for larger moons
    diameter = random.randint(50000, 400000)
    # Calculate gravity using scientific formula with gas giant density
    gravity = calculate_surface_gravity(diameter, density_kg_m3=1300)  # 1.3 g/cm³
    
    return PlanetSizeCategory(
        roll_min=2,
        roll_max=12,
        diameter_km=diameter,
        gravity_g=gravity,
        examples=["Gas Giant"]
    )
