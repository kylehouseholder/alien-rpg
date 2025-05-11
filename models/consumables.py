from equipment_item import ConsumableItem

# --- FOOD AND DRINK CONSUMABLES ---

prefab_meal = ConsumableItem(
    name="Prefab Meal",
    cost=10,
    weight=0.25,
    description="Standard pre-prepped rations served aboard most ships and stations.",
    supply_type="food",
    usage_tags=["consumable", "ration"],
    consumable=True
)

water_bottle = ConsumableItem(
    name="Water Bottle",
    cost=10,  # Using purified water default
    weight=0.25,
    description="Standard purified water used on ships or colonies.",
    supply_type="water",
    usage_tags=["consumable", "hydration"],
    consumable=True
)

bug_juice = ConsumableItem(
    name="Bug Juice Protein Drink",
    cost=5,
    weight=0.25,
    description="Nutrient-rich drink made from processed insects, cheap and sustaining.",
    supply_type="both",
    usage_tags=["consumable", "protein"],
    consumable=True
)

candy_bar = ConsumableItem(
    name="Candy Bar",
    cost=3,  # Average cost between 2–5
    weight=0.25,
    description="Luxury sugary snack common on the Frontier.",
    supply_type="food",
    usage_tags=["consumable", "snack"],
    consumable=True
)

carbonated_beverage = ConsumableItem(
    name="Carbonated Beverage",
    cost=2,
    weight=0.25,
    description="Bubbly drink providing temporary hydration.",
    supply_type="water",
    usage_tags=["consumable", "drink"],
    consumable=True
)

coffee = ConsumableItem(
    name="Coffee",
    cost=1,
    weight=0,
    description="Caffeinated brew that helps stave off exhaustion.",
    stress_effect=+1,
    usage_tags=["consumable", "stimulant"],
    consumable=True
)

beer = ConsumableItem(
    name="Beer",
    cost=4,
    weight=0.25,
    description="Standard alcoholic beverage common in colony bars.",
    stress_effect=-1,
    attribute_penalties={"WITS": -1},
    usage_tags=["consumable", "alcohol"],
    consumable=True
)

hard_liquor = ConsumableItem(
    name="Hard Liquor",
    cost=50,
    weight=1,
    description="High-proof spirits causing stronger mental impairment.",
    stress_effect=-1,
    attribute_penalties={"WITS": -1},
    usage_tags=["consumable", "alcohol"],
    consumable=True
)

colony_specialty_meal = ConsumableItem(
    name="Colony Specialty Meal",
    cost=100,
    weight=0.25,
    description="Unique local cuisine with calming psychological effects.",
    supply_type="food",
    stress_effect=-1,
    specialty=True,
    usage_tags=["consumable", "specialty"],
    consumable=True
)
