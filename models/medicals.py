from equipment_item import MedicalItem

# --- MEDICAL SUPPLIES ---

personal_medkit = MedicalItem(
    name="Personal Medkit",
    cost=50,
    weight=0.25,
    description="A compact field kit used to stabilize wounds and keep the injured mobile until further treatment is available.",
    skill_modifiers={"MEDICAL AID": +2},
    usage_tags=["medical"],
    limited_uses=1
)

surgical_kit = MedicalItem(
    name="Surgical Kit",
    cost=100,  # Average cost; some variability possible
    weight=0.5,
    description="A set of precision tools for field surgery—effective in saving lives or causing harm in a pinch.",
    skill_modifiers={"MEDICAL AID": +1},
    usage_tags=["medical", "combat"],
    weapon_properties={"bonus": +1, "damage": 2}
)

pauling_medpod = MedicalItem(
    name="Pauling MedPod",
    cost=2000000,
    weight=None,  # Considered fixed installation
    description="A high-end autonomous medical unit capable of complex surgical procedures and diagnostics.",
    medical_aid_level=10,
    programmable=True,
    usage_tags=["medical", "automated"]
)

autodoc = MedicalItem(
    name="AutoDoc",
    cost=500000,
    weight=None,  # Considered fixed installation
    description="A common automated medical station for basic treatment and trauma care aboard ships and stations.",
    medical_aid_level=6,
    programmable=True,
    usage_tags=["medical", "automated"]
)
