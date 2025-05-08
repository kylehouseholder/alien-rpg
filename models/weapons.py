from weapon_item import WeaponItem

# === PISTOLS ===
m4a3_service_pistol = WeaponItem(
    name="M4A3 Service Pistol",
    lore="This inexpensive 9mm pistol is the standard sidearm of the USCMC. You should always have a backup for your backup, and this pistol might as well be it.",
    bonus=2,
    damage=1,
    range="Medium",
    weight=0.5,
    cost=200,
    weapon_class="pistol",
    damage_type="ballistic",
    uses_ammo=True
)

magnum_357_revolver = WeaponItem(
    name=".357 Magnum Revolver",
    lore="A classic high caliber revolver, equally popular amongst both Frontier Marshals and lowlifes.",
    bonus=1,
    damage=2,
    range="Medium",
    weight=1,
    cost=300,
    weapon_class="pistol",
    damage_type="ballistic",
    uses_ammo=True
)

rexim_rxf_m5_eva_pistol = WeaponItem(
    name="Rexim RXF-M5 EVA Pistol",
    lore="A miniaturized and weaponized version of a Weyland-Yutani laser welder in use from the 2100-2120s. This tool was originally improvised as a weapon by the J’Har rebels during the 2106 uprising on Torin Prime. Always one to find profit in anything, Weyland-Yutani studied the modifications after the war and made them the standard self-defense armament on their commercial fleet.",
    bonus=1,
    damage=1,
    range="Medium",
    weight=0.5,
    cost=400,
    weapon_class="pistol",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing"
)

