import random
from models.worldbuilding import (
    generate_star_name, StarType, BrightnessClass, SpectralClass, Star,
    PlanetType, generate_orbital_body_name, get_planet_size_category,
    get_atmosphere_type, get_temperature_type, get_geosphere_type,
    get_planetary_terrain, get_ice_planet_terrain,
    get_colony_size, get_colony_mission, get_orbit_components,
    get_num_factions, get_colony_factions, get_colony_allegiance,
    AtmosphereType, ExplorationStatus, determine_exploration_status,
    get_moon_size_category, get_dwarf_planet_size, get_gas_giant_size,
    generate_asteroid_belt_name, generate_dwarf_planet_name, generate_gas_giant_name,
    generate_moon_name, generate_terrestrial_name, generate_colony_name,
    get_mythological_name, determine_colonization_status, ColonySize,
    OrbitalBody, ColonizationStatus, calculate_surface_gravity, get_colony_size_rank
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
                                parent_diameter_km: int = None, moon_index: int = None,
                                parent_name: str = None) -> OrbitalBody:
    """Generate and print details for any orbital body (planet or moon)."""
    # Determine exploration status
    exploration_roll = roll_2d6()
    exploration_status = determine_exploration_status(exploration_roll)
    
    # Create OrbitalBody instance
    body = OrbitalBody(
        name="",  # Will be set after generation
        type=body_type,
        exploration_status=exploration_status,
        colonization_status=ColonizationStatus.UNCOLONIZED,  # Default
        distance_au=distance_au,
        parent_star=star_name,
        moon_index=moon_index + 1 if moon_index is not None else None,  # Convert to 1-based index
        parent_name=parent_name  # Store parent name for moon naming
    )
    
    # Only show physical characteristics if the body has been at least detected
    if exploration_status != ExplorationStatus.UNDISCOVERED:
        # Size and physical characteristics
        if body_type == PlanetType.GAS_GIANT:
            size_cat = get_gas_giant_size()
        elif parent_diameter_km:  # This is a moon
            size_cat = get_moon_size_category(parent_diameter_km)
            # Ensure moon size is reasonable (max 25% of parent)
            max_size = parent_diameter_km * 0.25
            if size_cat.diameter_km > max_size:
                size_cat.diameter_km = int(max_size)
                # Recalculate gravity with new size
                size_cat.gravity_g = calculate_surface_gravity(size_cat.diameter_km)
        else:
            size_roll = roll_2d6()
            size_cat = get_planet_size_category(size_roll)
        
        body.size_category = size_cat  # Store size category for later use
        
        # Gas giant special reporting
        if body_type == PlanetType.GAS_GIANT:
            # Generate moons for gas giants
            num_moons = random.randint(1, 6)
            body.moons = []  # Initialize empty list, will be populated after naming
            return body
        
        # Initialize atmosphere and temperature variables
        atmosphere = None
        temperature = None
        
        # Only show detailed characteristics if surveyed or better
        if exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
            # Atmosphere
            atm_roll = roll_2d6()
            atmosphere = get_atmosphere_type(atm_roll, size_cat.diameter_km)
            body.atmosphere = atmosphere
            
            # Temperature
            temp_roll = roll_2d6()
            temperature = get_temperature_type(temp_roll, atmosphere)
            body.temperature = temperature
            
            # Geosphere
            geo_roll = roll_2d6()
            geosphere = get_geosphere_type(geo_roll, atmosphere, temperature)
            body.geosphere = geosphere
            
            # Terrain
            if body_type == PlanetType.ICE:
                terrain = get_ice_planet_terrain(roll_2d6())
                body.terrain = terrain
            else:
                terrain_roll = random.randint(11, 66)  # D66 roll
                terrain = get_planetary_terrain(terrain_roll)
                body.terrain = terrain
            
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
                # Determine colonization status
                colony_roll = roll_2d6()
                colonization_status = determine_colonization_status(colony_roll, has_colony=True)
                body.colonization_status = colonization_status
                
                # Colony size
                colony_roll = roll_2d6()
                colony_size = get_colony_size(colony_roll, atmosphere, size_cat.diameter_km)
                body.colony_size = colony_size.size
                
                # Colony mission
                mission_roll = roll_2d6()
                mission = get_colony_mission(mission_roll, colony_size.size, atmosphere)
                body.colony_mission = mission
                
                # Orbit components
                orbit_roll = roll_2d6()
                orbit = get_orbit_components(orbit_roll, colony_size.size)
                body.orbit = orbit
                
                # Factions
                num_factions = get_num_factions(random.randint(1, 6))
                factions = get_colony_factions(num_factions)
                body.factions = factions
                
                # Allegiance
                allegiance_roll = roll_3d6()
                allegiance = get_colony_allegiance(allegiance_roll)
                body.allegiance = allegiance
                
                # Generate colony name
                colony_name = generate_colony_name(colony_size.size, mission, allegiance)
                body.colony_name = colony_name
    
    return body

def print_body_details(body: OrbitalBody, star_name: str):
    """Print all details for a body."""
    print(f"\nName: {body.name}")
    
    # Display type with more descriptive names
    if body.type == PlanetType.TERRESTRIAL:
        print("Type: Terrestrial Planet")
    elif body.type == PlanetType.ICE:
        print("Type: Ice Planet")
    elif body.type == PlanetType.GAS_GIANT:
        print("Type: Gas Giant (GG)")
    elif body.type == PlanetType.ASTEROID_BELT:
        print("Type: Asteroid Belt (AST)")
    else:
        print(f"Type: {body.type.value}")
    
    print(f"Exploration Status: {body.exploration_status.value}")
    
    if body.type == PlanetType.ASTEROID_BELT:
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
            if body.exploration_status != ExplorationStatus.UNDISCOVERED:
                for dp_num in range(1, num_dwarf_planets + 1):
                    print(f"\nDwarf Planet {dp_num}:")
                    dp_size = get_dwarf_planet_size()
                    print(f"Size: {dp_size.diameter_km}km diameter")
                    print(f"Gravity: {dp_size.gravity_g}g")
                    
                    # Generate dwarf planet name with sequential number
                    dp_name = generate_dwarf_planet_name(star_name, dp_num)
                    print(f"Name: {dp_name}")
                    
                    if body.exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
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
    if body.exploration_status != ExplorationStatus.UNDISCOVERED:
        print(f"Size: {body.size_category.diameter_km}km diameter")
        print(f"Gravity: {body.size_category.gravity_g}g")
        
        # Gas giant special reporting
        if body.type == PlanetType.GAS_GIANT:
            print(f"Atmosphere Composition: {get_gas_giant_composition()}")
            print(f"Internal Structure: {get_gas_giant_structure()}")
            print("Note: Gas giants cannot be landed on; no solid surface.")
            
            if hasattr(body, 'moons'):
                print(f"\n--- Gas Giant Moons ({len(body.moons)}) ---")
                for moon in body.moons:
                    print_body_details(moon, star_name)
            return
        
        # Only show detailed characteristics if surveyed or better
        if body.exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
            print(f"Atmosphere: {body.atmosphere.value}")
            print(f"Temperature: {body.temperature.value}")
            print(f"Geosphere: {body.geosphere.value}")
            
            if isinstance(body.terrain, str):
                print(f"Terrain: {body.terrain}")
            else:
                print(f"Terrain: {body.terrain.value}")
            
            # Colony information
            if body.colonization_status != ColonizationStatus.UNCOLONIZED:
                print("\n--- Colony Information ---")
                print(f"Colonization Status: {body.colonization_status.value}")
                print(f"Size: {body.colony_size.value}")
                print(f"Mission: {body.colony_mission.value}")
                print(f"Orbit: {body.orbit.value}")
                print(f"Factions ({len(body.factions)}): {', '.join(f.value for f in body.factions)}")
                print(f"Allegiance: {body.allegiance.value}")
                print(f"Colony Name: {body.colony_name}")

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
    
    # Track all bodies for colony ranking
    all_bodies = []
    
    # First pass: Generate all bodies
    for distance in orbital_distances:
        # Basic body type - exclude dwarf planets from random selection
        planet_type = random.choice([t for t in PlanetType if t != PlanetType.DWARF_PLANET])
        
        # Generate body details
        body = generate_orbital_body_details(planet_type, distance, star.name)
        all_bodies.append(body)
    
    # Second pass: Name all bodies based on colony ranks
    colonized_bodies = [b for b in all_bodies if b.colonization_status != ColonizationStatus.UNCOLONIZED]
    if colonized_bodies:
        # Sort by colony size (ESTABLISHED > YOUNG > START_UP)
        colonized_bodies.sort(key=lambda b: get_colony_size_rank(b.colony_size) if hasattr(b, 'colony_size') else 0, reverse=True)
        
        # Update names based on rank
        for i, body in enumerate(colonized_bodies):
            if i == 0:  # Largest colony
                body.name = get_mythological_name()
            elif i == 1:  # Second largest colony
                body.name = f"{get_mythological_name()}-{star.name}"
    
    # Third pass: Name all remaining bodies
    for body in all_bodies:
        if not body.name:  # Only name bodies that haven't been named yet
            if body.type == PlanetType.ASTEROID_BELT:
                body.name = generate_asteroid_belt_name(star.name, body.distance_au)
            elif body.type == PlanetType.GAS_GIANT:
                body.name = generate_gas_giant_name(body, [], star.name)  # Empty moons list for now
            elif body.moon_index is not None:
                body.name = generate_moon_name(body, body.parent_name or star.name)
            else:
                body.name = generate_terrestrial_name(body, star.name)
    
    # Fourth pass: Generate moons for gas giants after they're named
    for body in all_bodies:
        if body.type == PlanetType.GAS_GIANT:
            num_moons = random.randint(1, 6)
            moons = []
            for moon_num in range(num_moons):
                moon = generate_orbital_body_details(PlanetType.TERRESTRIAL, body.distance_au, star.name,
                                                  body.size_category.diameter_km, moon_index=moon_num,
                                                  parent_name=body.name)
                moons.append(moon)
            body.moons = moons
    
    # Final pass: Print all details
    for body in all_bodies:
        print(f"\n--- Orbital Body at {body.distance_au} AU ---")
        print_body_details(body, star.name)

if __name__ == "__main__":
    # Generate a star system
    generate_star_system() 