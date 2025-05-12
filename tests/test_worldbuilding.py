import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import worldbuilding

# Star name generation
def test_generate_star_name():
    name = worldbuilding.generate_star_name()
    assert isinstance(name, str)
    assert len(name) > 0

# Planet size category
def test_get_planet_size_category():
    cat = worldbuilding.get_planet_size_category(7)
    assert hasattr(cat, 'diameter_km')
    assert cat.diameter_km > 0

# Atmosphere type
def test_get_atmosphere_type():
    atype = worldbuilding.get_atmosphere_type(7, 8000)
    assert atype in worldbuilding.AtmosphereType

# Temperature type
def test_get_temperature_type():
    ttype = worldbuilding.get_temperature_type(7, worldbuilding.AtmosphereType.BREATHABLE)
    assert ttype in worldbuilding.TemperatureType

# Geosphere type
def test_get_geosphere_type():
    gtype = worldbuilding.get_geosphere_type(7, worldbuilding.AtmosphereType.BREATHABLE, worldbuilding.TemperatureType.TEMPERATE)
    assert gtype in worldbuilding.GeosphereType

# Planetary terrain
def test_get_planetary_terrain():
    ttype = worldbuilding.get_planetary_terrain(33)
    assert ttype in worldbuilding.TerrainType

# Ice planet terrain
def test_get_ice_planet_terrain():
    desc = worldbuilding.get_ice_planet_terrain(7)
    assert isinstance(desc, str)
    assert len(desc) > 0

# Colony size
def test_get_colony_size():
    cat = worldbuilding.get_colony_size(7, worldbuilding.AtmosphereType.BREATHABLE, 8000)
    assert hasattr(cat, 'size')
    assert cat.size in worldbuilding.ColonySize

# Colony mission
def test_get_colony_mission():
    mtype = worldbuilding.get_colony_mission(7, worldbuilding.ColonySize.YOUNG, worldbuilding.AtmosphereType.BREATHABLE)
    assert mtype in worldbuilding.ColonyMissionType

# Orbit components
def test_get_orbit_components():
    otype = worldbuilding.get_orbit_components(7, worldbuilding.ColonySize.YOUNG)
    assert otype in worldbuilding.OrbitType

# Number of factions
def test_get_num_factions():
    n = worldbuilding.get_num_factions(6)
    assert 1 <= n <= 6

# Colony factions
def test_get_colony_factions():
    factions = worldbuilding.get_colony_factions(3)
    assert isinstance(factions, list)
    assert all(f in worldbuilding.FactionType for f in factions)

# Colony allegiance
def test_get_colony_allegiance():
    a = worldbuilding.get_colony_allegiance(7)
    assert a in worldbuilding.ColonyAllegiance 