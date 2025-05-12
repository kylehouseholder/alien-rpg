import random
from models.worldbuilding import (
    generate_star_name, StarType, BrightnessClass, SpectralClass, Star,
    PlanetType, generate_orbital_body_name, get_planet_size_category,
    get_atmosphere_type, get_temperature_type, get_geosphere_type,
    get_planetary_terrain, get_ice_planet_terrain,
    get_colony_size, get_colony_mission, get_orbit_components,
    get_num_factions, get_colony_factions, get_colony_allegiance,
    AtmosphereType, ExplorationStatus, determine_exploration_status,
    get_moon_size_category, get_dwarf_planet_size, get_gas_giant_size
)

def roll_2d6() -> int:
    """Simulate a 2d6 roll."""
    return random.randint(1, 6) + random.randint(1, 6)

def roll_3d6() -> int:
    """Simulate a 3d6 roll."""
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

# Add helper for gas giant composition and structure
GAS_GIANT_COMPOSITIONS = [
    "Hydrogen-Helium Dominant",
    "Hydrogen, Helium, Methane",
    "Hydrogen, Helium, Ammonia",
    "Hydrogen, Helium, Water Vapor",
    "Hydrogen, Helium, Trace Organics"
]
GAS_GIANT_STRUCTURES = [
    "Layers of metallic hydrogen, molecular hydrogen, and ices",
    "Thick gaseous envelope with a possible rocky/icy core",
    "No solid surface; gradual transition from gas to liquid",
    "Bands of clouds, storms, and high winds",
    "Deep atmosphere with complex weather systems"
]

def get_gas_giant_composition():
    return random.choice(GAS_GIANT_COMPOSITIONS)

def get_gas_giant_structure():
    return random.choice(GAS_GIANT_STRUCTURES)

def generate_orbital_body_details(body_type: PlanetType, distance_au: float, star_name: str, 
                                parent_diameter_km: int = None) -> None:
    """Generate and print details for any orbital body (planet or moon)."""
    # Determine exploration status
    exploration_roll = roll_2d6()
    exploration_status = determine_exploration_status(exploration_roll)
    
    # Generate name based on star and exploration status
    name = generate_orbital_body_name(star_name, body_type, distance_au, exploration_status)
    print(f"Name: {name}")
    
    # Display type with more descriptive names
    if body_type == PlanetType.TERRESTRIAL:
        print("Type: Terrestrial Planet")
    elif body_type == PlanetType.ICE:
        print("Type: Ice Planet")
    else:
        print(f"Type: {body_type.value}")
    
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
                print(f"\nMoon {moon_num + 1}:")
                generate_orbital_body_details(PlanetType.TERRESTRIAL, distance_au, star_name, size_cat.diameter_km)
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

def generate_star_system():
    """Generate and display a complete star system."""
    print("\n=== STAR SYSTEM GENERATION ===")
    
    # Generate star
    star_name = generate_star_name()
    star_type = random.choice(list(StarType))
    brightness = random.choice(list(BrightnessClass))
    spectral = random.choice(list(SpectralClass))
    star = Star(star_name, star_type, brightness, spectral)
    
    print(f"\nStar: {star.name}")
    print(f"Type: {star.star_type.value}")
    print(f"Brightness: {star.brightness_class.value}")
    print(f"Spectral Class: {star.spectral_class.value}")
    
    # Generate orbital bodies
    num_bodies = random.randint(3, 8)
    print(f"\nGenerating {num_bodies} orbital bodies...")
    
    # Generate orbital distances (in AU)
    orbital_distances = sorted([round(random.uniform(0.4, 30.0), 2) for _ in range(num_bodies)])
    
    for i, distance in enumerate(orbital_distances):
        print(f"\n--- Orbital Body at {distance} AU ---")
        
        # Basic body type
        planet_type = random.choice(list(PlanetType))
        
        # Generate body details
        generate_orbital_body_details(planet_type, distance, star.name)

if __name__ == "__main__":
    # Generate a star system
    generate_star_system() 