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
    OrbitalBody, ColonizationStatus, calculate_surface_gravity, get_colony_size_rank,
    OrbitalSystem
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

def calculate_hill_sphere_radius(moon_diameter_km: int, parent_diameter_km: int, 
                               moon_distance_km: int) -> float:
    """
    Calculate the Hill sphere radius for a moon.
    R_h = a * (m/3M)^(1/3)
    where:
    - a is the moon's orbital distance
    - m is the moon's mass
    - M is the parent planet's mass
    
    We'll use diameter ratios as a proxy for mass ratios since we don't have exact masses.
    """
    # Convert diameters to masses (assuming similar densities)
    moon_mass_ratio = (moon_diameter_km / parent_diameter_km) ** 3
    return moon_distance_km * (moon_mass_ratio / 3) ** (1/3)

def determine_exploration_status_for_body(body_type: PlanetType, roll: int) -> ExplorationStatus:
    """Determine exploration status, capping at 'surveyed' for gas giants and asteroid belts."""
    status = determine_exploration_status(roll)
    if body_type in [PlanetType.GAS_GIANT, PlanetType.ASTEROID_BELT]:
        if status == ExplorationStatus.EXPLORED:
            return ExplorationStatus.SURVEYED
    return status

def generate_orbital_body_details(body_type: PlanetType, distance_au: float, star_name: str, 
                                parent_diameter_km: int = None, moon_index: int = None,
                                parent_name: str = None) -> OrbitalBody:
    """Generate details for any orbital body (planet or moon)."""
    # Determine exploration status
    exploration_roll = roll_2d6()
    exploration_status = determine_exploration_status_for_body(body_type, exploration_roll)
    
    # Create OrbitalBody instance
    body = OrbitalBody(
        name="",  # Will be set during naming phase
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
        elif body_type == PlanetType.ASTEROID_BELT:
            # Asteroid belts don't have meaningful gravity
            size_cat = None
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
        
        # Only show detailed characteristics if surveyed or better
        if exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
            # For asteroid belts, skip atmosphere/temperature/geosphere
            if body_type != PlanetType.ASTEROID_BELT:
                # Atmosphere
                atm_roll = roll_2d6()
                atmosphere = get_atmosphere_type(atm_roll, size_cat.diameter_km)
                body.atmosphere = atmosphere
                
                # Temperature
                temp_roll = roll_2d6()
                temperature = get_temperature_type(temp_roll, atmosphere, body_type)
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
            can_have_colony = False
            
            # Check if body type can have colonies
            if body_type in [PlanetType.TERRESTRIAL, PlanetType.ICE]:
                # For terrestrial planets, check gravity restrictions
                if body_type == PlanetType.TERRESTRIAL:
                    can_have_colony = 0.6 <= size_cat.gravity_g <= 1.5
                
                # For ice planets, check special colonization conditions
                elif body_type == PlanetType.ICE:
                    conditions_met = 0
                    
                    # 1. Volcanic Activity
                    if isinstance(body.terrain, str) and any(volcanic in body.terrain.lower() for volcanic in 
                        ['volcanic', 'thermal', 'steam', 'lava']):
                        conditions_met += 1
                    
                    # 2. Subsurface Ocean
                    if ((body.temperature.value == 'Cold' and 
                         body.geosphere.value in ['Temperate-Wet World', 'Wet World']) or
                        (body.temperature.value == 'Frozen' and 
                         body.geosphere.value == 'Volcanic World')):
                        conditions_met += 1
                    
                    # 3. Breathable/Filterable Atmosphere
                    if body.atmosphere.value in ['Breathable', 'Thin']:
                        conditions_met += 1
                    
                    # 4. Rare/Valuable Resource
                    if (isinstance(body.terrain, str) and 
                        any(resource in body.terrain.lower() for resource in 
                            ['salt', 'silicon', 'mineral', 'crystal'])) or \
                       body.geosphere.value == 'Desert World':
                        conditions_met += 1
                    
                    # 5. Low Gravity
                    if size_cat.gravity_g < 0.7:
                        conditions_met += 1
                    
                    # Need at least 2 conditions for colonization
                    can_have_colony = conditions_met >= 2
            
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

def generate_star_system():
    """Generate and display a complete star system."""
    print("\n=== STAR SYSTEM GENERATION ===")
    
    # Generate star
    star_name = generate_star_name()
    star_type = random.choice(list(StarType))
    brightness = random.choice(list(BrightnessClass))
    spectral = random.choice(list(SpectralClass))
    star = Star(star_name, star_type, brightness, spectral)
    
    # Create main system
    system = OrbitalSystem(id="A", name=star_name)
    
    print(f"\nStar: {star.name}")
    print(f"Type: {star.star_type.value}")
    print(f"Brightness: {star.brightness_class.value}")
    print(f"Spectral Class: {star.spectral_class.value}")
    
    # Generate orbital bodies
    num_bodies = random.randint(3, 8)
    print(f"\nGenerating {num_bodies} orbital bodies...")
    
    # Generate orbital distances (in AU)
    orbital_distances = sorted([round(random.uniform(0.4, 30.0), 2) for _ in range(num_bodies)])
    
    # First pass: Generate all bodies with hierarchical IDs
    for i, distance in enumerate(orbital_distances, 1):
        # Basic body type - exclude dwarf planets from random selection
        planet_type = random.choice([t for t in PlanetType if t != PlanetType.DWARF_PLANET])
        
        # Generate body details
        body = generate_orbital_body_details(planet_type, distance, star.name)
        body.id = f"A.{i}"  # Assign hierarchical ID
        system.add_body(body)
        
        # If this is a gas giant, generate its moon system
        if planet_type == PlanetType.GAS_GIANT:
            gas_giant_system = OrbitalSystem(id=f"A.{i}", parent_id="A")
            num_moons = random.randint(1, 6)
            
            # Calculate safe maximum distance for moons
            # Use 1/3 of the distance to the next planet (if any) as a safe maximum
            next_planet_distance = None
            prev_planet_distance = None
            
            # Get distances to neighboring planets
            if i < len(orbital_distances):
                next_planet_distance = orbital_distances[i]
            if i > 1:
                prev_planet_distance = orbital_distances[i-2]  # i-2 because i is 1-based
            
            # Convert AU to km for calculations (1 AU = 149,597,870.7 km)
            current_au = distance
            
            # Calculate maximum safe distance based on both inner and outer planets
            max_moon_distance_au = None
            
            if next_planet_distance:
                # Distance to next planet
                max_moon_distance_au = (next_planet_distance - current_au) / 3
            
            if prev_planet_distance:
                # Distance to previous planet
                prev_max = (current_au - prev_planet_distance) / 3
                if max_moon_distance_au is None:
                    max_moon_distance_au = prev_max
                else:
                    # Use the smaller of the two distances
                    max_moon_distance_au = min(max_moon_distance_au, prev_max)
            
            if max_moon_distance_au is None:
                # If no neighboring planets, use 1/10 of distance from star
                max_moon_distance_au = current_au / 10
            
            max_moon_distance_km = int(max_moon_distance_au * 149597870.7)
            
            # Ensure minimum and maximum moon distances are reasonable
            min_moon_distance = 400000  # 400,000 km minimum
            max_moon_distance = min(max_moon_distance_km, 2000000)  # Cap at 2 million km
            
            # Generate all moons
            moons = []
            used_moons = []  # Track both distance and moon object
            
            for moon_num in range(num_moons):
                # First generate the moon to get its size
                moon = generate_orbital_body_details(
                    PlanetType.TERRESTRIAL,
                    distance,  # Use the parent's distance from star
                    star.name,
                    body.size_category.diameter_km if body.size_category else None,
                    moon_index=moon_num,
                    parent_name=body.name
                )
                
                # Skip if moon doesn't have a size category
                if not moon.size_category:
                    continue
                
                # Calculate this moon's Hill sphere radius
                moon_hill_sphere = calculate_hill_sphere_radius(
                    moon.size_category.diameter_km,
                    body.size_category.diameter_km if body.size_category else 100000,  # Default to 100,000 km if no size
                    min_moon_distance  # Use minimum distance as initial guess
                )
                
                # Try to find a valid distance that doesn't conflict with existing moons
                max_attempts = 10  # Prevent infinite loops
                attempts = 0
                while attempts < max_attempts:
                    # Generate a random distance
                    distance = random.randint(min_moon_distance, max_moon_distance)
                    
                    # Check if this distance is too close to any existing moon
                    # Use 5 times the sum of Hill sphere radii as minimum separation
                    too_close = any(
                        abs(distance - existing_moon[0]) < 5 * (moon_hill_sphere + 
                            calculate_hill_sphere_radius(
                                existing_moon[1].size_category.diameter_km if existing_moon[1].size_category else 100000,
                                body.size_category.diameter_km if body.size_category else 100000,
                                existing_moon[0]
                            ))
                        for existing_moon in used_moons
                    )
                    
                    if not too_close:
                        used_moons.append((distance, moon))
                        break
                    attempts += 1
                
                if attempts == max_attempts:
                    # If we couldn't find a valid distance, skip this moon
                    continue
                
                moon.distance_from_parent_km = distance
                moon.id = f"A.{i}.{moon_num + 1}"
                moons.append(moon)
            
            # Sort moons by distance from parent
            moons.sort(key=lambda m: m.distance_from_parent_km)
            
            # Add sorted moons to the system
            for moon in moons:
                gas_giant_system.add_body(moon)
            
            body.moon_system = gas_giant_system
    
    # Calculate exploration scores
    system._update_exploration_scores()
    
    # Naming phase
    # First, check if system deserves a proper name
    if system.get_exploration_percentage() > 50:  # Lowered threshold to 50%
        system.name = get_mythological_name()
        # Update all body names to reference the system name
        for body in system.bodies:
            if body.type == PlanetType.ASTEROID_BELT:
                body.name = f"{system.name}-AST-{int(body.distance_au * 10)}"
            elif body.type == PlanetType.GAS_GIANT:
                # Check if gas giant deserves its own name
                if hasattr(body, 'moon_system'):
                    moon_system = body.moon_system
                    # Check if gas giant or any moon has a colony
                    has_colony = (body.colonization_status != ColonizationStatus.UNCOLONIZED or
                                any(m.colonization_status != ColonizationStatus.UNCOLONIZED 
                                   for m in moon_system.bodies))
                    # Check moon system exploration percentage
                    moon_exploration = moon_system.get_exploration_percentage()
                    
                    if has_colony or moon_exploration >= 90:
                        # Gas giant gets its own mythological name
                        gas_giant_name = get_mythological_name()
                        body.name = gas_giant_name
                    else:
                        body.name = f"{system.name}-GG-{int(body.distance_au * 10)}"
                else:
                    body.name = f"{system.name}-GG-{int(body.distance_au * 10)}"
            elif body.type == PlanetType.ICE:
                body.name = f"{system.name}-IP-{int(body.distance_au * 10)}"
            else:
                body.name = f"{system.name}-TP-{int(body.distance_au * 10)}"
            
            # Name moons for gas giants
            if body.type == PlanetType.GAS_GIANT and hasattr(body, 'moon_system'):
                letter_index = 0  # For continuous letter sequence
                undiscovered_count = 0  # For undiscovered moon numbering
                
                for moon in body.moon_system.bodies:
                    if moon.exploration_status == ExplorationStatus.UNDISCOVERED:
                        undiscovered_count += 1
                        moon.name = f"{body.name}-uex*-{undiscovered_count}"
                    else:
                        # Convert letter_index to letter (0->a, 1->b, etc.)
                        moon_letter = chr(ord('a') + letter_index)
                        moon.name = f"{body.name}{moon_letter}"
                        letter_index += 1
    else:
        # System doesn't get a mythological name, but bodies still need designations
        system.name = star.name  # Use the star's designation as the system name
        letter_index = 0  # For continuous letter sequence
        undiscovered_count = 0  # For undiscovered body numbering
        
        for body in system.bodies:
            if body.exploration_status == ExplorationStatus.UNDISCOVERED:
                undiscovered_count += 1
                if body.type == PlanetType.ASTEROID_BELT:
                    body.name = f"{system.name}-AST-uex*-{undiscovered_count}"
                elif body.type == PlanetType.GAS_GIANT:
                    body.name = f"{system.name}-GG-uex*-{undiscovered_count}"
                elif body.type == PlanetType.ICE:
                    body.name = f"{system.name}-IP-uex*-{undiscovered_count}"
                else:
                    body.name = f"{system.name}-TP-uex*-{undiscovered_count}"
            else:
                # Convert letter_index to letter (0->a, 1->b, etc.)
                body_letter = chr(ord('a') + letter_index)
                if body.type == PlanetType.ASTEROID_BELT:
                    body.name = f"{system.name}-AST-{body_letter}"
                elif body.type == PlanetType.GAS_GIANT:
                    # Check if gas giant deserves its own name
                    if hasattr(body, 'moon_system'):
                        moon_system = body.moon_system
                        # Check if gas giant or any moon has a colony
                        has_colony = (body.colonization_status != ColonizationStatus.UNCOLONIZED or
                                    any(m.colonization_status != ColonizationStatus.UNCOLONIZED 
                                       for m in moon_system.bodies))
                        # Check moon system exploration percentage
                        moon_exploration = moon_system.get_exploration_percentage()
                        
                        if has_colony or moon_exploration >= 90:
                            # Gas giant gets its own mythological name
                            gas_giant_name = get_mythological_name()
                            body.name = gas_giant_name
                        else:
                            body.name = f"{system.name}-GG-{body_letter}"
                    else:
                        body.name = f"{system.name}-GG-{body_letter}"
                elif body.type == PlanetType.ICE:
                    body.name = f"{system.name}-IP-{body_letter}"
                else:
                    body.name = f"{system.name}-TP-{body_letter}"
                letter_index += 1
            
            # Name moons for gas giants
            if body.type == PlanetType.GAS_GIANT and hasattr(body, 'moon_system'):
                moon_letter_index = 0  # For continuous letter sequence
                moon_undiscovered_count = 0  # For undiscovered moon numbering
                
                for moon in body.moon_system.bodies:
                    if moon.exploration_status == ExplorationStatus.UNDISCOVERED:
                        moon_undiscovered_count += 1
                        moon.name = f"{body.name}-uex*-{moon_undiscovered_count}"
                    else:
                        # Convert letter_index to letter (0->a, 1->b, etc.)
                        moon_letter = chr(ord('a') + moon_letter_index)
                        moon.name = f"{body.name}{moon_letter}"
                        moon_letter_index += 1
    
    # Print all details
    print_system_details(system)

def print_system_details(system: OrbitalSystem, indent: str = ""):
    """Print all details for a system and its bodies."""
    print(f"\n{indent}System: {system.name} (ID: {system.id})")
    print(f"{indent}Exploration: {system.exploration_score:.1f}/{system.max_exploration_score:.1f} ({system.get_exploration_percentage():.1f}%)")
    
    for body in system.bodies:
        print(f"\n{indent}--- Orbital Body at {body.distance_au} AU ---")
        print(f"{indent}Name: {body.name}")
        print(f"{indent}Type: {body.type.value}")
        if body.moon_index is not None:  # This is a moon
            print(f"{indent}Distance from parent: {body.distance_from_parent_km:,} km")
        print(f"{indent}Exploration Status: {body.exploration_status.value} (Score: {system._get_actual_score_for_body(body):.1f}/{system._get_max_score_for_body(body):.1f})")
        
        if body.exploration_status != ExplorationStatus.UNDISCOVERED:
            if body.type != PlanetType.ASTEROID_BELT:
                print(f"{indent}Size: {body.size_category.diameter_km}km diameter")
                print(f"{indent}Gravity: {body.size_category.gravity_g}g")
            
            if body.type == PlanetType.GAS_GIANT:
                print(f"{indent}Atmosphere Composition: {get_gas_giant_composition()}")
                print(f"{indent}Internal Structure: {get_gas_giant_structure()}")
                print(f"{indent}Note: Gas giants cannot be landed on; no solid surface.")
                
                if hasattr(body, 'moon_system'):
                    print(f"\n{indent}--- Gas Giant Moons ({len(body.moon_system.bodies)}) ---")
                    print_system_details(body.moon_system, indent + "  ")
            
            elif body.exploration_status in [ExplorationStatus.SURVEYED, ExplorationStatus.EXPLORED]:
                if body.atmosphere is not None:
                    print(f"{indent}Atmosphere: {body.atmosphere.value}")
                if body.temperature is not None:
                    print(f"{indent}Temperature: {body.temperature.value}")
                if body.geosphere is not None:
                    print(f"{indent}Geosphere: {body.geosphere.value}")
                if body.terrain is not None:
                    if isinstance(body.terrain, str):
                        print(f"{indent}Terrain: {body.terrain}")
                    else:
                        print(f"{indent}Terrain: {body.terrain.value}")
                
                if body.colonization_status != ColonizationStatus.UNCOLONIZED:
                    print(f"\n{indent}--- Colony Information ---")
                    print(f"{indent}Colonization Status: {body.colonization_status.value}")
                    print(f"{indent}Size: {body.colony_size.value}")
                    print(f"{indent}Mission: {body.colony_mission.value}")
                    print(f"{indent}Orbit: {body.orbit.value}")
                    print(f"{indent}Factions ({len(body.factions)}): {', '.join(f.value for f in body.factions)}")
                    print(f"{indent}Allegiance: {body.allegiance.value}")
                    print(f"{indent}Colony Name: {body.colony_name}")

if __name__ == "__main__":
    # Generate a star system
    generate_star_system() 