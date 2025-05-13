import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Union
import os
import json
import math

# Constants for gravity calculations
G = 6.67430e-11  # Gravitational constant in m³/kg/s²
EARTH_MASS = 5.972e24  # Earth's mass in kg
EARTH_RADIUS = 6371000  # Earth's radius in meters
EARTH_GRAVITY = 9.81  # Earth's surface gravity in m/s²
DEFAULT_DENSITY = 4500  # Default density in kg/m³ (4.5 g/cm³) - average of terrestrial planets

class PlanetType(Enum):
    """Categories of planetary bodies."""
    TERRESTRIAL = 'Terrestrial'
    GAS_GIANT = 'Gas Giant'
    ICE = 'Ice'
    ASTEROID_BELT = 'Asteroid Belt'
    DWARF_PLANET = 'Dwarf Planet'

# Name pools for different naming conventions
GREEK_LETTERS = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
CATALOG_PREFIXES = ['HR','HD','Gliese']
SECTOR_LETTERS = [chr(c) for c in range(ord('A'),ord('Z')+1)]
SECTOR_DIGITS = list(range(1,10))
ALPHANUM_PREFIXES = ['SYS','XQ','ZT']

# Name pools for colonized worlds vs unsurveyed bodies
INHABITED_PLANET_NAMES = [
    'Hannibal','Monos','Requiem','Nakaya','Phaeton','Nocturne','Prospero',
    'Magdala','Hamilton','Tracatus','Aurora','Arges','Damnation','Nero',
    'Doramin','Solitude','Euphrates','Nemesis','Moab','Steropes','Napier'
]

# Prefixes for different types of bodies
PLANET_PREFIX_MAP = {
    PlanetType.TERRESTRIAL: ["TP", "Terra", "Tellus"],
    PlanetType.ICE: ["IP", "Glacius", "Frost"],
    PlanetType.GAS_GIANT: ["GG", "Jovian", "Giant"],
    PlanetType.ASTEROID_BELT: ["AST", "Belt", "Ring"],
    PlanetType.DWARF_PLANET: ["DP", "Dwarf", "Minor"]
}

def roll_2d6() -> int:
    """Simulate a 2d6 roll."""
    return random.randint(1, 6) + random.randint(1, 6)

def roll_3d6() -> int:
    """Simulate a 3d6 roll."""
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

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

class ColonySize(Enum):
    """Size categories for colonies."""
    START_UP = 'Start-Up'
    YOUNG = 'Young'
    ESTABLISHED = 'Established'

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

def get_moon_letter(index: int) -> str:
    """
    Convert a moon index to a letter designation.
    For example: 1 -> 'a', 2 -> 'b', etc.
    After 'z', it goes to 'aa', 'ab', etc.
    """
    if index <= 0:
        raise ValueError("Moon index must be positive")
    
    # Convert to 0-based index
    index -= 1
    
    # Calculate how many letters we need
    num_letters = (index // 26) + 1
    
    # Generate the letter sequence
    result = ""
    remaining = index
    for _ in range(num_letters):
        result = chr(ord('a') + (remaining % 26)) + result
        remaining //= 26
    
    return result

def get_system_naming_level(colonies: List[ColonySize]) -> int:
    """
    Determine the naming level of a system based on its colonies.
    Returns:
    0: No colonies (catalog designations only)
    1: Start-up colonies (star may be named)
    2: Young colonies (star and major planets may be named)
    3: Established colonies (all significant bodies may be named)
    """
    if not colonies:
        return 0
    
    # Count colony sizes
    start_ups = sum(1 for c in colonies if c == ColonySize.START_UP)
    young = sum(1 for c in colonies if c == ColonySize.YOUNG)
    established = sum(1 for c in colonies if c == ColonySize.ESTABLISHED)
    
    # Determine naming level
    if established > 0:
        return 3
    elif young > 0:
        return 2
    elif start_ups > 0:
        return 1
    return 0

class ExplorationStatus(Enum):
    """Possible exploration states for orbital bodies."""
    UNDISCOVERED = "Undiscovered"  # Not even detected by ICC
    DETECTED = "Detected"          # Known to exist but unexplored
    SURVEYED = "Surveyed"          # Basic survey completed
    EXPLORED = "Explored"          # Detailed exploration completed

class ColonizationStatus(Enum):
    """Possible colonization states for orbital bodies."""
    UNCOLONIZED = "Uncolonized"    # No permanent settlement
    COLONY = "Colony"              # Has a permanent settlement
    COLONIZED = "Colonized"        # Fully colonized world

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
# COLONY GENERATION: Colony Size, Missions, Orbits, Factions, Allegiance
# ===========================================================================

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

def get_colony_size_rank(colony_size: ColonySize) -> int:
    """Convert colony size to a numeric rank."""
    return {
        ColonySize.START_UP: 1,
        ColonySize.YOUNG: 2,
        ColonySize.ESTABLISHED: 3
    }[colony_size]

@dataclass
class OrbitalBody:
    """Represents any orbital body with exploration and colonization status."""
    name: str
    type: PlanetType
    exploration_status: ExplorationStatus
    colonization_status: ColonizationStatus
    distance_au: float
    parent_star: str  # Name of the parent star
    colony_name: Optional[str] = None  # Name of the colony if present
    moon_index: Optional[int] = None  # Index of the moon if it's a moon
    parent_name: Optional[str] = None  # Name of the parent body if it's a moon
    size_category: Optional[PlanetSizeCategory] = None  # Size and gravity information
    atmosphere: Optional[AtmosphereType] = None  # Atmosphere type if known
    temperature: Optional[TemperatureType] = None  # Temperature type if known
    geosphere: Optional[GeosphereType] = None  # Geosphere type if known
    terrain: Optional[Union[str, TerrainType]] = None  # Terrain type if known
    colony_size: Optional[ColonySize] = None  # Colony size if colonized
    colony_mission: Optional[ColonyMissionType] = None  # Colony mission if colonized
    orbit: Optional[OrbitType] = None  # Orbit type if colonized
    factions: Optional[List[FactionType]] = None  # Factions present if colonized
    allegiance: Optional[ColonyAllegiance] = None  # Allegiance if colonized
    moons: Optional[List['OrbitalBody']] = None  # List of moons if this is a gas giant

class ExplorationPoints:
    """Constants for exploration point values."""
    UNDISCOVERED = 0
    DETECTED = 1
    SURVEYED = 2
    EXPLORED = 3
    COLONIZED = 4

@dataclass
class SystemExplorationStatus:
    """Tracks exploration status of a star system."""
    total_possible_points: int
    actual_points: int
    percentage: float

def calculate_exploration_points(exploration_status: ExplorationStatus, 
                               has_colony: bool = False) -> int:
    """Calculate points for a single body's exploration status."""
    if has_colony:
        return ExplorationPoints.COLONIZED
    return {
        ExplorationStatus.UNDISCOVERED: ExplorationPoints.UNDISCOVERED,
        ExplorationStatus.DETECTED: ExplorationPoints.DETECTED,
        ExplorationStatus.SURVEYED: ExplorationPoints.SURVEYED,
        ExplorationStatus.EXPLORED: ExplorationPoints.EXPLORED
    }[exploration_status]

def calculate_system_exploration(orbital_bodies: List[OrbitalBody]) -> SystemExplorationStatus:
    """
    Calculate the exploration status of an entire system.
    
    Args:
        orbital_bodies: List of all orbital bodies in the system
        
    Returns:
        SystemExplorationStatus with total possible points, actual points, and percentage
    """
    total_possible = 0
    actual_points = 0
    
    for body in orbital_bodies:
        # Calculate possible points for this body
        if body.type in [PlanetType.TERRESTRIAL, PlanetType.ICE]:
            # These can be colonized
            total_possible += ExplorationPoints.COLONIZED
        else:
            # Gas giants, asteroid belts, etc. can only be explored
            total_possible += ExplorationPoints.EXPLORED
        
        # Add actual points
        actual_points += calculate_exploration_points(
            body.exploration_status,
            body.colonization_status != ColonizationStatus.UNCOLONIZED
        )
    
    # Calculate percentage
    percentage = (actual_points / total_possible) * 100 if total_possible > 0 else 0
    
    return SystemExplorationStatus(total_possible, actual_points, percentage)

def generate_star_name(style: Optional[int] = None, 
                      system_exploration: Optional[SystemExplorationStatus] = None) -> str:
    """
    Create a star name based on exploration status and style.
    
    Args:
        style: Optional naming style (1-4)
        system_exploration: Optional SystemExplorationStatus for the star system
        
    Returns:
        str: A name for the star
    """
    # If we have exploration data, use it to determine naming style
    if system_exploration:
        if system_exploration.percentage >= 75:  # High exploration
            # 90% chance of mythological name
            if random.random() < 0.9:
                return get_mythological_name()
        elif system_exploration.percentage >= 50:  # Medium exploration
            # 50% chance of mythological name with designation
            if random.random() < 0.5:
                return f"{get_mythological_name()}-{generate_catalog_designation()}"
    
    # If no exploration data or below thresholds, use catalog designation
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

def generate_catalog_designation() -> str:
    """Generate a catalog designation for a star."""
    style = random.choice([1,2,3])
    if style == 1:
        return f"{random.choice(CATALOG_PREFIXES)} {random.choice(GREEK_LETTERS)}-{random.randint(1,20)}"
    elif style == 2:
        return f"{random.choice(SECTOR_LETTERS)}{random.choice(SECTOR_DIGITS)}-{random.choice(SECTOR_DIGITS)}{random.choice(SECTOR_LETTERS)}"
    else:
        return f"{random.choice(ALPHANUM_PREFIXES)}-{random.randint(100,999)}"

# ===========================================================================
# PLANETS: Types, Naming & Features
# ===========================================================================

def get_gas_giant_moon_count() -> int:
    """
    Gas giants inherently host a sizable satellite system: roll 1d6 and add 4
    to determine the number of significant moons (regardless of orbit table).
    """
    return random.randint(1, 6) + 4

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

def determine_colonization_status(roll: int, has_colony: bool = False) -> ColonizationStatus:
    """
    Determine colonization status based on a 2d6 roll.
    """
    if has_colony:
        if roll >= 10:
            return ColonizationStatus.COLONIZED
        return ColonizationStatus.COLONY
    return ColonizationStatus.UNCOLONIZED

def generate_orbital_body_details(body_type: PlanetType, distance_au: float, star_name: str, 
                                parent_diameter_km: int = None, moon_index: int = None,
                                parent_name: str = None) -> None:
    """Generate and print details for any orbital body (planet or moon)."""
    # Determine exploration status
    exploration_roll = roll_2d6()
    exploration_status = determine_exploration_status(exploration_roll)
    
    # Generate name based on star and exploration status
    # Convert moon_index to 1-based for get_moon_letter
    name = generate_orbital_body_name(star_name, body_type, distance_au, exploration_status,
                                    moon_index=moon_index + 1 if moon_index is not None else None,
                                    parent_name=parent_name)
    
    # Display type with more descriptive names
    type_str = "Terrestrial Planet" if body_type == PlanetType.TERRESTRIAL else \
               "Ice Planet" if body_type == PlanetType.ICE else \
               f"{body_type.value}"
    
    # Print complete information for this body
    print(f"\nName: {name}")
    print(f"Type: {type_str}")
    print(f"Exploration Status: {exploration_status.value}")
    
    if body_type == PlanetType.ASTEROID_BELT:
        # Asteroid belt specific generation
        mining_roll = roll_2d6()
        dwarf_planet_roll = roll_2d6()
        
        # Mining operations (10+ on 2d6)
        has_mining = mining_roll >= 10
        print(f"Mining Operations: {'Yes' if has_mining else 'No'}")
    
        # Dwarf planets (10+ on 2d6)
        has_dwarf_planets = dwarf_planet_roll >= 10
        if has_dwarf_planets:
            num_dwarf_planets = random.randint(1, 3)
            print(f"Contains {num_dwarf_planets} dwarf planet(s)")
    
            # Generate dwarf planet details if explored
            if exploration_status != ExplorationStatus.UNDISCOVERED:
                for dp in range(num_dwarf_planets):
                    print(f"\nDwarf Planet {dp + 1}:")
                    dp_size = get_dwarf_planet_size()
                    print(f"Size: {dp_size.diameter_km}km diameter")
                    print(f"Gravity: {dp_size.gravity_g}g")
                    
                    # Generate dwarf planet name
                    dp_name = generate_orbital_body_name(star_name, PlanetType.ASTEROID_BELT, 
                                                       distance_au, exploration_status, 
                                                       is_dwarf_planet=True)
                    print(f"Name: {dp_name}")
                    
                    if exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
                        dp_atm_roll = roll_2d6()
                        dp_atmosphere = get_atmosphere_type(dp_atm_roll, dp_size.diameter_km)
                        print(f"Atmosphere: {dp_atmosphere.value}")
                        
                        dp_temp_roll = roll_2d6()
                        dp_temperature = get_temperature_type(dp_temp_roll, dp_atmosphere)
                        print(f"Temperature: {dp_temperature.value}")
        
        # Special features (12 on 2d6)
        if mining_roll == 12:
            print("Special Feature: Major mining operation with permanent station")
        elif dwarf_planet_roll == 12:
            print("Special Feature: Dwarf planet shows signs of ancient alien activity")
        
        return
    
    # Only show physical characteristics if the body has been at least detected
    if exploration_status != ExplorationStatus.UNDISCOVERED:
        # Size and physical characteristics
        if body_type == PlanetType.GAS_GIANT:
            size_cat = get_gas_giant_size()
        elif parent_diameter_km:  # This is a moon
            size_cat = get_moon_size_category(parent_diameter_km)
        else:
            size_roll = roll_2d6()
            size_cat = get_planet_size_category(size_roll)
        
        print(f"Size: {size_cat.diameter_km}km diameter")
        print(f"Gravity: {size_cat.gravity_g}g")
        
        # Gas giant special reporting
        if body_type == PlanetType.GAS_GIANT:
            print(f"Atmosphere Composition: {get_gas_giant_composition()}")
            print(f"Internal Structure: {get_gas_giant_structure()}")
            print("Note: Gas giants cannot be landed on; no solid surface.")
            # Generate moons for gas giants
            num_moons = random.randint(1, 6)
            print(f"\n--- Gas Giant Moons ({num_moons}) ---")
            for moon_num in range(num_moons):
                generate_orbital_body_details(PlanetType.TERRESTRIAL, distance_au, star_name, 
                                           size_cat.diameter_km, moon_index=moon_num,
                                           parent_name=name)
            return
        
        # Initialize atmosphere and temperature variables
        atmosphere = None
        temperature = None
        
        # Only show detailed characteristics if surveyed or better
        if exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
            # Atmosphere
            atm_roll = roll_2d6()
            atmosphere = get_atmosphere_type(atm_roll, size_cat.diameter_km)
            print(f"Atmosphere: {atmosphere.value}")
            
            # Temperature
            temp_roll = roll_2d6()
            temperature = get_temperature_type(temp_roll, atmosphere)
            print(f"Temperature: {temperature.value}")
            
            # Geosphere
            geo_roll = roll_2d6()
            geosphere = get_geosphere_type(geo_roll, atmosphere, temperature)
            print(f"Geosphere: {geosphere.value}")
            
            # Terrain
            if body_type == PlanetType.ICE:
                terrain = get_ice_planet_terrain(roll_2d6())
                print(f"Terrain: {terrain}")
            else:
                terrain_roll = random.randint(11, 66)  # D66 roll
                terrain = get_planetary_terrain(terrain_roll)
                print(f"Terrain: {terrain.value}")
            
            # Colony generation (if applicable)
            can_have_colony = True
            
            # Check gravity restrictions
            if body_type == PlanetType.ICE:
                # Ice planets need breathable atmosphere and specific gravity range
                can_have_colony = (atmosphere == AtmosphereType.BREATHABLE and 
                                 0.8 <= size_cat.gravity_g <= 1.2)
                if can_have_colony:
                    # Even if conditions are met, only 20% chance of colony
                    can_have_colony = random.random() < 0.2
            else:
                # Other terrestrial planets need reasonable gravity
                can_have_colony = 0.6 <= size_cat.gravity_g <= 1.5
            
            if can_have_colony and random.random() < 0.3:  # 30% chance of having a colony
                print("\n--- Colony Information ---")
                
                # Determine colonization status
                colony_roll = roll_2d6()
                colonization_status = determine_colonization_status(colony_roll, has_colony=True)
                print(f"Colonization Status: {colonization_status.value}")
                
                # Colony size
                colony_roll = roll_2d6()
                colony_size = get_colony_size(colony_roll, atmosphere, size_cat.diameter_km)
                print(f"Size: {colony_size.size.value}")
                
                # Colony mission
                mission_roll = roll_2d6()
                mission = get_colony_mission(mission_roll, colony_size.size, atmosphere)
                print(f"Mission: {mission.value}")
                
                # Orbit components
                orbit_roll = roll_2d6()
                orbit = get_orbit_components(orbit_roll, colony_size.size)
                print(f"Orbit: {orbit.value}")
                
                # Factions
                num_factions = get_num_factions(random.randint(1, 6))
                factions = get_colony_factions(num_factions)
                print(f"Factions ({num_factions}): {', '.join(f.value for f in factions)}")
                
                # Allegiance
                allegiance_roll = roll_3d6()
                allegiance = get_colony_allegiance(allegiance_roll)
                print(f"Allegiance: {allegiance.value}")
                
                # Generate colony name
                colony_name = generate_colony_name(colony_size.size, mission, allegiance)
                print(f"Colony Name: {colony_name}")

def determine_exploration_status(roll: int) -> ExplorationStatus:
    """
    Determine exploration status based on a 2d6 roll.
    """
    if roll <= 3:
        return ExplorationStatus.UNDISCOVERED
    elif roll <= 6:
        return ExplorationStatus.DETECTED
    elif roll <= 9:
        return ExplorationStatus.SURVEYED
    else:
        return ExplorationStatus.EXPLORED

def get_gas_giant_composition() -> str:
    """Return a random gas giant composition."""
    compositions = [
        "Hydrogen-Helium Dominant",
        "Hydrogen, Helium, Methane",
        "Hydrogen, Helium, Ammonia",
        "Hydrogen, Helium, Water Vapor",
        "Hydrogen, Helium, Trace Organics"
    ]
    return random.choice(compositions)

def get_gas_giant_structure() -> str:
    """Return a random gas giant structure description."""
    structures = [
        "Layers of metallic hydrogen, molecular hydrogen, and ices",
        "Thick gaseous envelope with a possible rocky/icy core",
        "No solid surface; gradual transition from gas to liquid",
        "Bands of clouds, storms, and high winds",
        "Deep atmosphere with complex weather systems"
    ]
    return random.choice(structures)

def get_dwarf_planet_size() -> PlanetSizeCategory:
    """
    Generate a size category for a dwarf planet.
    Dwarf planets are typically between 800-2300km in diameter.
    """
    # Generate a random diameter between 800-2300km
    diameter = random.randint(800, 2300)
    
    # Dwarf planets are typically icy bodies, so use a lower density
    # Density varies between 1.8-2.2 g/cm³ (1800-2200 kg/m³)
    density = random.randint(1800, 2200)
    
    # Calculate gravity using scientific formula
    gravity = calculate_surface_gravity(diameter, density_kg_m3=density)
    
    return PlanetSizeCategory(
        roll_min=2,
        roll_max=12,
        diameter_km=diameter,
        gravity_g=gravity,
        examples=["Dwarf Planet"]
    )

def get_gas_giant_size() -> PlanetSizeCategory:
    """
    Generate a size category for a gas giant.
    Gas giants are typically between 30,000-140,000km in diameter.
    """
    # Generate a random diameter between 30,000-140,000km
    diameter = random.randint(30000, 140000)
    
    # Gas giants have very low density
    # Density varies between 0.6-1.3 g/cm³ (600-1300 kg/m³)
    density = random.randint(600, 1300)
    
    # Calculate gravity using scientific formula
    gravity = calculate_surface_gravity(diameter, density_kg_m3=density)
    
    return PlanetSizeCategory(
        roll_min=2,
        roll_max=12,
        diameter_km=diameter,
        gravity_g=gravity,
        examples=["Gas Giant"]
    )

def get_moon_size_category(parent_diameter_km: int) -> PlanetSizeCategory:
    """
    Generate a size category for a moon that is appropriately smaller than its parent body.
    The moon's diameter will be between 2-12% of the parent's diameter.
    There's also a chance (25%) of a "super moon" that's 12-25% of the parent's diameter.
    """
    # Roll for super moon chance (25% chance)
    is_super_moon = random.random() < 0.25
    
    if is_super_moon:
        # Super moon: 12-25% of parent diameter
        min_diameter = int(parent_diameter_km * 0.12)
        max_diameter = int(parent_diameter_km * 0.25)
    else:
        # Normal moon: 2-12% of parent diameter
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
        if moon_diameter > 15000:
            density = 5500  # 5.5 g/cm³ for larger rocky moons
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

def generate_colony_name(colony_size: ColonySize, mission: ColonyMissionType, 
                        allegiance: ColonyAllegiance) -> str:
    """
    Generate a name for a colony based on its characteristics.
    
    Args:
        colony_size: Size of the colony
        mission: Primary mission of the colony
        allegiance: Corporate or government allegiance
    
    Returns:
        str: A name for the colony
    """
    # Mission-specific name components
    mission_prefixes = {
        ColonyMissionType.TERRAFORMING: ['Nova', 'Genesis', 'Terra', 'Gaia', 'Eden'],
        ColonyMissionType.RESEARCH: ['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma'],
        ColonyMissionType.SURVEY_PROSPECT: ['Prospect', 'Survey', 'Scout', 'Pioneer', 'Frontier'],
        ColonyMissionType.PRISON: ['Penal', 'Exile', 'Isolation', 'Confinement', 'Restriction'],
        ColonyMissionType.MINING_REFINING: ['Mine', 'Refinery', 'Extraction', 'Ore', 'Mineral'],
        ColonyMissionType.MINERAL_DRILLING: ['Drill', 'Core', 'Bore', 'Shaft', 'Tunnel'],
        ColonyMissionType.COMMS_RELAY: ['Relay', 'Beacon', 'Signal', 'Transmit', 'Broadcast'],
        ColonyMissionType.MILITARY: ['Base', 'Fort', 'Outpost', 'Station', 'Command'],
        ColonyMissionType.CATTLE_LOGGING: ['Ranch', 'Range', 'Forest', 'Timber', 'Wood'],
        ColonyMissionType.CORPORATE_HQ: ['Hub', 'Center', 'Nexus', 'Core', 'Prime'],
        ColonyMissionType.GOVT_HQ: ['Capital', 'Center', 'Hub', 'Seat', 'Base']
    }
    
    # Size-specific suffixes
    size_suffixes = {
        ColonySize.START_UP: ['Point', 'Site', 'Post', 'Camp', 'Station'],
        ColonySize.YOUNG: ['Colony', 'Settlement', 'Outpost', 'Base', 'Hub'],
        ColonySize.ESTABLISHED: ['City', 'Metropolis', 'Center', 'Capital', 'Hub']
    }
    
    # Corporate-specific name components
    corporate_elements = {
        ColonyAllegiance.WEYLAND: ['Weyland', 'Yutani', 'WeyTech', 'WeyCorp'],
        ColonyAllegiance.SEEGSON: ['Seegson', 'SeegTech', 'SeegCorp'],
        ColonyAllegiance.GUSTAFSSON: ['Gustafsson', 'GustCorp', 'GustTech'],
        ColonyAllegiance.KELLAND: ['Kelland', 'KellCorp', 'KellTech'],
        ColonyAllegiance.GEOFUND: ['GeoFund', 'GeoCorp', 'GeoBase'],
        ColonyAllegiance.JINGTI: ['Jingti', 'JingCorp', 'JingTech'],
        ColonyAllegiance.CHIGUSA: ['Chigusa', 'ChigCorp', 'ChigTech'],
        ColonyAllegiance.LASALLE: ['Lasalle', 'LasCorp', 'LasTech'],
        ColonyAllegiance.LORENZ: ['Lorenz', 'LorCorp', 'LorTech'],
        ColonyAllegiance.GEMINI: ['Gemini', 'GemCorp', 'GemTech'],
        ColonyAllegiance.FARSIDE: ['Farside', 'FarCorp', 'FarTech']
    }
    
    # 40% chance to use a mythological name
    if random.random() < 0.4:
        myth_name = get_mythological_name()
        # 30% chance to add a corporate element
        if allegiance != ColonyAllegiance.NONE and random.random() < 0.3:
            corp_element = random.choice(corporate_elements[allegiance])
            return f"{corp_element} {myth_name}"
        return myth_name
    
    # 30% chance to use a corporate name with a unique identifier
    if allegiance != ColonyAllegiance.NONE and random.random() < 0.3:
        corp_element = random.choice(corporate_elements[allegiance])
        # Add a unique identifier (mythological name or mission-specific element)
        if random.random() < 0.5:
            identifier = get_mythological_name()
        else:
            identifier = random.choice(mission_prefixes[mission])
        return f"{corp_element} {identifier}"
    
    # Otherwise, create a thematic name
    prefix = random.choice(mission_prefixes[mission])
    suffix = random.choice(size_suffixes[colony_size])
    
    # 40% chance to add a unique element
    if random.random() < 0.4:
        if random.random() < 0.5:
            # Add a mythological name
            unique_element = get_mythological_name()
            return f"{prefix} {unique_element} {suffix}"
        else:
            # Add a Greek letter or number
            if random.random() < 0.5:
                return f"{prefix} {random.choice(GREEK_LETTERS)} {suffix}"
            else:
                return f"{prefix} {random.randint(1,9)} {suffix}"
    
    return f"{prefix} {suffix}"

def get_mythological_name() -> str:
    """
    Return a random mythological name from a curated list.
    These names are chosen to be evocative and memorable.
    """
    mythological_names = [
        # Greek/Roman
        'Atlas', 'Prometheus', 'Pandora', 'Icarus', 'Orion', 'Perseus', 'Hercules',
        'Achilles', 'Odysseus', 'Theseus', 'Jason', 'Medea', 'Ariadne', 'Dionysus',
        'Apollo', 'Artemis', 'Athena', 'Zeus', 'Hera', 'Poseidon', 'Hades', 'Demeter',
        'Hestia', 'Aphrodite', 'Ares', 'Hephaestus', 'Hermes', 'Persephone', 'Eros',
        
        # Norse
        'Odin', 'Thor', 'Loki', 'Freyja', 'Freyr', 'Heimdall', 'Tyr', 'Baldur',
        'Hel', 'Fenrir', 'Jormungandr', 'Sleipnir', 'Yggdrasil', 'Valhalla',
        
        # Egyptian
        'Ra', 'Osiris', 'Isis', 'Horus', 'Anubis', 'Thoth', 'Seth', 'Bastet',
        'Sekhmet', 'Hathor', 'Ptah', 'Sobek', 'Khonsu', 'Ma\'at',
        
        # Mesopotamian
        'Gilgamesh', 'Enkidu', 'Ishtar', 'Marduk', 'Tiamat', 'Apsu', 'Ea',
        'Nergal', 'Nabu', 'Shamash', 'Sin', 'Adad',
        
        # Hindu
        'Indra', 'Agni', 'Varuna', 'Vayu', 'Surya', 'Chandra', 'Yama',
        'Kubera', 'Vishnu', 'Shiva', 'Brahma', 'Kali', 'Durga', 'Ganesha',
        
        # Chinese
        'Fuxi', 'Nuwa', 'Pangu', 'Yu', 'Chang\'e', 'Houyi', 'Jingwei',
        'Kuafu', 'Nezha', 'Sun Wukong', 'Yanluo', 'Zhong Kui',
        
        # Japanese
        'Amaterasu', 'Susanoo', 'Tsukuyomi', 'Izanagi', 'Izanami', 'Raijin',
        'Fujin', 'Hachiman', 'Inari', 'Benzaiten', 'Daikokuten', 'Ebisu',
        
        # Celtic
        'Lugh', 'Dagda', 'Morrigan', 'Brigid', 'Cernunnos', 'Aengus',
        'Manannan', 'Nuada', 'Ogma', 'Dian Cecht', 'Goibniu', 'Lir',
        
        # Slavic
        'Perun', 'Veles', 'Svarog', 'Dazhbog', 'Stribog', 'Mokosh',
        'Rod', 'Svarozhich', 'Zorya', 'Koschei', 'Baba Yaga', 'Leshy',
        
        # Aztec
        'Quetzalcoatl', 'Tezcatlipoca', 'Huitzilopochtli', 'Tlaloc',
        'Chalchiuhtlicue', 'Xipe Totec', 'Mictlantecuhtli', 'Coatlicue',
        
        # Mayan
        'Itzamna', 'Kukulkan', 'Chaac', 'Ixchel', 'Ah Puch', 'Hunahpu',
        'Xbalanque', 'Vucub Caquix', 'Zipacna', 'Cabracan',
        
        # Polynesian
        'Maui', 'Pele', 'Tane', 'Rongo', 'Tangaroa', 'Tawhiri', 'Haumia',
        'Ruaumoko', 'Whiro', 'Hine-nui-te-po',
        
        # African
        'Anansi', 'Ogun', 'Shango', 'Oya', 'Yemoja', 'Oshun', 'Obatala',
        'Eshu', 'Olorun', 'Olokun', 'Orunmila', 'Ogun',
        
        # Native American
        'Coyote', 'Raven', 'Thunderbird', 'Nanabozho', 'Gluskap', 'Iktomi',
        'Sedna', 'Trickster', 'Manabozho', 'Wakinyan',
        
        # Modern/Contemporary
        'Nova', 'Pulsar', 'Quasar', 'Nebula', 'Cosmos', 'Stellar', 'Celestial',
        'Astral', 'Ethereal', 'Cosmic', 'Galactic', 'Interstellar', 'Quantum',
        'Nebulous', 'Stellar', 'Astral', 'Ethereal', 'Cosmic', 'Galactic'
    ]
    return random.choice(mythological_names)

def generate_orbital_body_name(star_name: str, body_type: PlanetType, distance_au: float,
                             exploration_status: ExplorationStatus, moon_index: int = None,
                             parent_name: str = None, is_dwarf_planet: bool = False) -> str:
    """
    Generate a name for an orbital body based on its characteristics and exploration status.
    
    Args:
        star_name: Name of the parent star
        body_type: Type of the orbital body
        distance_au: Distance from star in AU
        exploration_status: Current exploration status
        moon_index: Index of the moon (if it's a moon)
        parent_name: Name of the parent body (if it's a moon)
        is_dwarf_planet: Whether this is a dwarf planet
    
    Returns:
        str: A name for the orbital body
    """
    # For moons, use a letter designation with hyphen
    if moon_index is not None:
        moon_letter = get_moon_letter(moon_index)
        if parent_name:
            return f"{parent_name}-{moon_letter}"
        return f"{star_name}-{moon_letter}"
    
    # For dwarf planets in asteroid belts
    if is_dwarf_planet:
        # Use sequential numbering starting from 1
        dwarf_num = random.randint(1, 9)  # This should be passed in from the parent
        return f"{star_name}-Dwarf-{dwarf_num}"
    
    # For asteroid belts, always use AST designation
    if body_type == PlanetType.ASTEROID_BELT:
        distance_code = f"{int(distance_au * 10):02d}"
        return f"AST-{distance_code}-{random.randint(1,999):03d}"
    
    # For undiscovered bodies, use a special designation
    if exploration_status == ExplorationStatus.UNDISCOVERED:
        prefix = random.choice(PLANET_PREFIX_MAP[body_type])
        return f"{prefix}-uex-{random.randint(1,999):03d}"
    
    # For detected bodies, use a more specific catalog designation
    if exploration_status == ExplorationStatus.DETECTED:
        prefix = random.choice(PLANET_PREFIX_MAP[body_type])
        # Add distance information
        distance_code = f"{int(distance_au * 10):02d}"
        return f"{prefix}-{distance_code}-{random.randint(1,999):03d}"
    
    # For surveyed bodies, use a catalog designation with a small chance of a name
    if exploration_status == ExplorationStatus.SURVEYED:
        # 20% chance for a mythological name
        if random.random() < 0.2:
            return get_mythological_name()
        # Otherwise use catalog designation
        prefix = random.choice(PLANET_PREFIX_MAP[body_type])
        distance_code = f"{int(distance_au * 10):02d}"
        return f"{prefix}-{distance_code}-{random.randint(1,999):03d}"
    
    # For explored bodies, higher chance of a name but still not guaranteed
    if exploration_status == ExplorationStatus.EXPLORED:
        # 60% chance for a mythological name
        if random.random() < 0.6:
            return get_mythological_name()
        # Otherwise use catalog designation
        prefix = random.choice(PLANET_PREFIX_MAP[body_type])
        distance_code = f"{int(distance_au * 10):02d}"
        return f"{prefix}-{distance_code}-{random.randint(1,999):03d}"
    
    # Fallback to a catalog designation
    prefix = random.choice(PLANET_PREFIX_MAP[body_type])
    distance_code = f"{int(distance_au * 10):02d}"
    return f"{prefix}-{distance_code}-{random.randint(1,999):03d}"

def calculate_gas_giant_exploration(gas_giant: OrbitalBody, moons: List[OrbitalBody]) -> SystemExplorationStatus:
    """
    Calculate the exploration status of a gas giant and its moons.
    
    Args:
        gas_giant: The gas giant OrbitalBody
        moons: List of moon OrbitalBodies
        
    Returns:
        SystemExplorationStatus with total possible points, actual points, and percentage
    """
    total_possible = ExplorationPoints.EXPLORED  # Gas giant can only be explored
    actual_points = calculate_exploration_points(gas_giant.exploration_status)
    
    # Add moon points
    for moon in moons:
        # Moons can be colonized
        total_possible += ExplorationPoints.COLONIZED
        actual_points += calculate_exploration_points(
            moon.exploration_status,
            moon.colonization_status != ColonizationStatus.UNCOLONIZED
        )
    
    # Calculate percentage
    percentage = (actual_points / total_possible) * 100 if total_possible > 0 else 0
    
    return SystemExplorationStatus(total_possible, actual_points, percentage)

def generate_gas_giant_name(gas_giant: OrbitalBody, moons: List[OrbitalBody], 
                          star_designation: str) -> str:
    """
    Generate a name for a gas giant based on its exploration status and that of its moons.
    
    Args:
        gas_giant: The gas giant OrbitalBody
        moons: List of moon OrbitalBodies
        star_designation: The designation of the parent star
        
    Returns:
        str: A name for the gas giant
    """
    exploration = calculate_gas_giant_exploration(gas_giant, moons)
    
    if exploration.percentage >= 75:  # High exploration
        # 80% chance of mythological name
        if random.random() < 0.8:
            return get_mythological_name()
    elif exploration.percentage >= 50:  # Medium exploration
        # 40% chance of mythological name with designation
        if random.random() < 0.4:
            return f"{get_mythological_name()}-{star_designation}"
    
    # Otherwise use catalog designation
    return f"{star_designation}-GG-{int(gas_giant.distance_au * 10):02d}"

def get_colony_size_rank(colony_size: ColonySize) -> int:
    """Convert colony size to a numeric rank."""
    return {
        ColonySize.START_UP: 1,
        ColonySize.YOUNG: 2,
        ColonySize.ESTABLISHED: 3
    }[colony_size]

def generate_terrestrial_name(body: OrbitalBody, star_designation: str,
                            colony_rank: Optional[int] = None) -> str:
    """
    Generate a name for a terrestrial or ice planet based on exploration and colony status.
    
    Args:
        body: The OrbitalBody
        star_designation: The designation of the parent star
        colony_rank: Optional rank of this body's colony (1 = largest, 2 = second largest, etc.)
        
    Returns:
        str: A name for the body
    """
    # If it has a colony, use colony rank to determine naming
    if colony_rank is not None:
        if colony_rank == 1:  # Largest colony
            return get_mythological_name()
        elif colony_rank == 2:  # Second largest colony
            return f"{get_mythological_name()}-{star_designation}"
    
    # If explored but no colony or lower rank colony
    if body.exploration_status == ExplorationStatus.EXPLORED:
        # 30% chance of mythological name
        if random.random() < 0.3:
            return get_mythological_name()
    
    # Otherwise use catalog designation
    prefix = "TP" if body.type == PlanetType.TERRESTRIAL else "IP"
    return f"{star_designation}-{prefix}-{int(body.distance_au * 10):02d}"

def generate_moon_name(moon: OrbitalBody, parent_name: str,
                      colony_rank: Optional[int] = None) -> str:
    """
    Generate a name for a moon based on exploration and colony status.
    
    Args:
        moon: The moon OrbitalBody
        parent_name: The name of the parent body
        colony_rank: Optional rank of this moon's colony
        
    Returns:
        str: A name for the moon
    """
    # If it has a colony, use colony rank to determine naming
    if colony_rank is not None:
        if colony_rank == 1:  # Largest colony
            return get_mythological_name()
        elif colony_rank == 2:  # Second largest colony
            return f"{get_mythological_name()}-{parent_name}"
    
    # If explored but no colony or lower rank colony
    if moon.exploration_status == ExplorationStatus.EXPLORED:
        # 20% chance of mythological name
        if random.random() < 0.2:
            return get_mythological_name()
    
    # Otherwise use letter designation
    return f"{parent_name}-{get_moon_letter(moon.moon_index)}"

def generate_asteroid_belt_name(star_designation: str, distance_au: float) -> str:
    """Generate a name for an asteroid belt."""
    return f"{star_designation}-AST-{distance_au:.1f}AU"

def generate_dwarf_planet_name(star_designation: str, sequence_number: int) -> str:
    """Generate a name for a dwarf planet."""
    return f"{star_designation}-DWF-{sequence_number}"
