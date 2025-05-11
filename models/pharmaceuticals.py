from equipment_item import PharmaceuticalItem

# --- PHARMACEUTICALS ---

neversleep_pills = PharmaceuticalItem(
    name="Neversleep Pills",
    cost=2,
    weight=0.01,
    description="Stimulant that eliminates the need for sleep for one day, at the cost of increased stress.",
    effects=["Gain +1 STRESS LEVEL", "Do not need to sleep for one day"],
    usage_tags=["drug", "stimulant"],
    consumable=True
)

hydr8tion = PharmaceuticalItem(
    name="Hydr8tion",
    cost=5,
    weight=0.01,
    description="An electrolyte solution that negates dehydration effects from hypersleep.",
    effects=["Removes Dehydration from hypersleep"],
    usage_tags=["drug", "recovery"],
    consumable=True
)

naproleve = PharmaceuticalItem(
    name="Naproleve",
    cost=20,
    weight=0.01,
    description="Powerful injectable stress reliever with intoxicating side effects if overused.",
    effects=["Reduce STRESS LEVEL to 0", "Subsequent doses in same Shift: -1 to AGILITY-based skill rolls"],
    usage_tags=["drug", "sedative"],
    consumable=True
)

recreational_drugs = PharmaceuticalItem(
    name="Recreational Drugs",
    cost=100,  # Placeholder average
    weight=0.01,
    description="Includes cannabis, tobacco, and legal psychoactives. Effects vary.",
    effects=["Effect varies by substance"],
    usage_tags=["drug", "recreational"],
    consumable=True,
    addictive=True
)

x_drugs = PharmaceuticalItem(
    name="X-Drugs",
    cost=500,  # Black-market average
    weight=0.01,
    description="Potent illegal stimulants that enhance abilities with dangerous side effects.",
    effects=["Enhances physical traits", "Risk of hallucinations, seizures, psychosis, stroke"],
    usage_tags=["drug", "experimental"],
    consumable=True,
    addictive=True,
    black_market=True
)
