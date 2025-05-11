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

watatsumi_dv303_bolt_gun = WeaponItem(
    name="Watatsumi DV-303 Bolt Gun",
    lore="The DV-303 is a construction tool that uses expanding bolts to make emergency hull repairs. The DV-303 can be turned into an improvised weapon—firing bolts like a single round shotgun—a trick first used by Frontier rebels in the early 2100s. This weapon must be reloaded after each shot.",
    bonus=0,
    damage=3,
    range="Short",
    weight=1,
    cost=400,
    weapon_class="pistol",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing",
    single_shot=True
)

bionational_tx9_chemical_air_pistol = WeaponItem(
    name="Bionational TX-9 Chemical Air Pistol",
    lore="A short-range injection pistol capable of delivering toxins, bioweapons, or biochemical tracers. While not very damaging, its true lethality comes from the payload it delivers. Tracer darts can mark a target for days, detectable at long distances.",
    bonus=1,
    damage=1,
    max_damage=1,
    range="Medium",
    weight=0.5,
    cost=300,
    weapon_class="pistol",
    damage_type="piercing",
    armor_effect="armor_doubled",
    special_effect="Delivers toxins or bioweapons"
)

vp_70ma6_semi_automatic_pistol = WeaponItem(
    name="VP-70MA6 Semi-Automatic Pistol",
    lore="A time-honored sidearm with a legacy spanning nearly two centuries. Once exclusive to USCMC officers from influential military families, the VP-70MA6 has gradually become the standard issue sidearm for Marines across the colonies, replacing the aging M4A3.",
    bonus=2,
    damage=1,
    range="Medium",
    weight=0.5,
    cost=250,
    weapon_class="pistol",
    damage_type="ballistic"
)

weyland_es4_electrostatic_pistol = WeaponItem(
    name="Weyland ES-4 Semi-Automatic Electrostatic Pistol",
    lore="Once favored by corporate security teams, the ES-4 fires high-speed electrostatic rounds that deliver a potent stun effect on impact. Although known for its distinctive blue muzzle flash and reliability, its upkeep requirements saw it fall out of widespread use before the Weyland-Yutani merger. Some colonial marshals have begun testing it again on the Frontier.",
    bonus=1,
    damage=1,
    range="Medium",
    weight=0.5,
    cost=1000,
    weapon_class="pistol",
    damage_type="stun",
    armor_effect="armor_piercing",
    special_effect="Stun on hit (STAMINA -2, lose slow action for 1 round)",
    malfunction_risk="If 2+ Stress ONES are rolled, shooter is stunned"
)

norcomm_qsz203_semi_automatic_pistol = WeaponItem(
    name="Norcomm QSZ-203 Semi-Automatic Pistol",
    lore="The standard issue sidearm of the UPP since 2164, the QSZ-203 is a rugged and reliable short recoil-operated pistol. Known for its durability and armor-piercing rounds, it serves as a companion to the AK-4047 Pulse Rifle and is a hallmark of Norcomm’s robust military production.",
    bonus=1,
    damage=1,
    range="Medium",
    weight=0.5,
    cost=400,
    weapon_class="pistol",
    damage_type="ballistic",
    armor_effect="armor_piercing"
)

m72_starshell_flare_pistol = WeaponItem(
    name="M72 Starshell Flare Pistol",
    lore="An emergency pistol issued on most military and civilian atmospheric vehicles. When fired vertically, the Starshell illuminates one zone for several rounds. In a pinch, it can be used as a weapon—though it's not designed for direct combat.",
    bonus=1,
    damage=1,
    range="Medium",
    weight=0.25,
    cost=50,
    weapon_class="pistol",
    damage_type="special",
    critical_override="#15 if used to inflict a critical injury",
    special_effect="Illuminates one zone for D6 rounds"
)

rexim_rxf_m5a3_eva_pistol = WeaponItem(
    name="Rexim RXF-M5A3 EVA Pistol",
    lore="An upgraded version of the standard Rexim EVA Pistol, issued across the Weyland-Yutani fleet. Outfitted with a 4×20 scope and an underslung LAG light dial for adjustable fire intensity.",
    bonus=1,
    damage=1,
    range="Medium",
    weight=1,
    cost=500,
    weapon_class="pistol",
    damage_type="ballistic",
    armor_effect="armor piercing",
    special_effect="Includes scope and LAG light dial for adjustable damage"
)

hyperdyne_357_frontier_revolver = WeaponItem(
    name="Hyperdyne .357 Frontier Revolver",
    lore="A compact and powerful sidearm favored on the Frontier for its affordability and ease of ownership. Though reliable, its reload process is slow, requiring manual insertion of each round.",
    bonus=1,
    damage=2,
    range="Medium",
    weight=1,
    cost=200,
    weapon_class="pistol",
    damage_type="ballistic",
    single_shot=True,
    special_effect="Manual reload: 2 rounds per fast or slow action"
)

gorham_44_magnum_pistol = WeaponItem(
    name="Gorham .44 Magnum Pistol",
    lore="Named after a famed pioneer colonist, this heavy handgun delivers powerful high-velocity slugs. Known for its devastating recoil, it's not suited for those with lower physical strength.",
    bonus=0,
    damage=2,
    range="Medium",
    weight=1,
    cost=600,
    weapon_class="pistol",
    damage_type="ballistic",
    armor_effect="armor_piercing",
    user_condition_penalty="−1 RANGED COMBAT if Strength < 3"
)


upp_mp_4043_grach_special = WeaponItem(
    name="MP-4043 Grach Special",
    lore="The pinnacle of UPP small arms engineering, the 4043 Grach Special is reserved for senior officers who earn the right to wield it. Combining refined aesthetics with modern reliability, it marks a major evolution in the Grach series.",
    bonus=2,
    damage=2,
    range="Medium",
    weight=1,
    cost=1800,
    weapon_class="pistol",
    damage_type="ballistic",
    armor_effect="armor_piercing"
)


# === RIFLES ===

armat_m41a_pulse_rifle = WeaponItem(
    name="Armat M41A Pulse Rifle",
    lore="The standard issue weapon of the USCMC, the M41A Pulse Rifle is a 10mm automatic assault rifle with an underslung 30mm grenade launcher. It fires explosive-tip caseless rounds and is known for its reliability, though it can jam when fully loaded. Marines are advised to partially load magazines to avoid jams.",
    bonus=1,
    damage=2,
    range="Long",
    weight=1,
    cost=1200,
    weapon_class="rifle",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing",
    full_auto=True,
    secondary_weapon="U1 Grenade Launcher"
)

ak4047_pulse_assault_rifle = WeaponItem(
    name="AK-4047 Pulse Assault Rifle",
    lore="The UPP equivalent to the M41A Pulse Rifle, the AK-4047 is a cheap and reliable substitute. Though less accurate, it is renowned for its extreme durability—able to function after being thrown off a cliff or submerged for extended periods.",
    bonus=0,
    damage=2,
    range="Long",
    weight=1,
    cost=500,
    weapon_class="rifle",
    damage_type="ballistic",
    uses_ammo=True,
    full_auto=True
)

armat_m42a_scope_rifle = WeaponItem(
    name="Armat M42A Scope Rifle",
    lore="Equipped with a folding bipod, muzzle flash suppressor, and adjustable stock, the M42A is the USCMC’s semi-automatic sniper rifle of choice. Ideal for eliminating targets spotted before they become a threat.",
    bonus=2,
    damage=2,
    range="Extreme",
    weight=1,
    cost=1000,
    weapon_class="rifle",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing"
)

armat_model_37a2_shotgun = WeaponItem(
    name="Armat Model 37A2 12 Gauge Pump Action",
    lore="A classic pump-action combat shotgun, the M37A2 is reliable and favored for close encounters. It remains a popular choice among USCMC personnel as a straightforward and devastating weapon at short range.",
    bonus=2,
    damage=3,
    range="Short",
    weight=1,
    cost=500,
    weapon_class="rifle",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_doubled"
)

armat_xm99a_phased_plasma_rifle = WeaponItem(
    name="Armat XM99A Phased Plasma Pulse Rifle",
    lore="A powerful prototype weapon being tested by the USCMC, the XM99A is capable of killing most targets in a single shot. The plasma charge requires careful aiming and introduces a brief delay before firing. Each shot consumes significant energy, necessitating a Power Supply roll after every use.",
    bonus=0,
    damage=4,
    range="Extreme",
    weight=2,
    cost=20000,
    weapon_class="rifle",
    damage_type="energy",
    uses_ammo=True,
    armor_effect="armor_piercing",
    power_supply=5
)

spacesub_asso400_harpoon_gun = WeaponItem(
    name="SpaceSub ASSO-400 Harpoon Grappling Gun",
    lore="Designed for aiding in emergency manual docking maneuvers, the ASSO-400 fires a grappling hook with a tether. It can be used to rappel toward a heavier target or pull lighter targets closer, making it an essential tool in EVA situations.",
    bonus=0,
    damage=1,
    range="Medium",
    weight=1,
    cost=300,
    weapon_class="rifle",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_doubled",
    single_shot=True,
    special_effect="grapple"
)

armat_p9_sharp_rifle = WeaponItem(
    name="Armat P9 S.H.A.R.P. Rifle",
    lore="The prototype Sonic Harpoon Artillery Remote Projectile Rifle (S.H.A.R.P.) fires specialized darts that either detonate after a short delay or instantly on direct hits. Favored for its area denial capabilities, the P9 uses sticky explosive charges that trigger devastating explosions when targets move within its deadly zone.",
    bonus=0,
    damage=0,
    blast_power=9,
    range="Long",
    weight=2,
    cost=15000,
    weapon_class="rifle",
    damage_type="blast",
    armor_effect="armor_piercing",
    detonation_trigger="Detonates after 1 Round or immediately if a target moves in the zone",
    direct_target_bonus="+2 damage and armor piercing on direct hit"
)

norcomm_ak4047_pulse_assault_rifle = WeaponItem(
    name="Norcomm AK-4047 Pulse Assault Rifle",
    lore="A rugged and affordable alternative to the USCMC's M41A, the AK-4047 has become a common sight in the hands of mercenaries and insurgents across the Frontier. Though less accurate, it is famously durable, capable of withstanding brutal conditions without failure.",
    bonus=0,
    damage=2,
    range="Long",
    weight=1,
    cost=500,
    weapon_class="rifle",
    damage_type="ballistic",
    full_auto=True
)

norcomm_ak104s_pulse_action_suit_gun = WeaponItem(
    name="Norcomm AK-104S Pulse Action Suit Gun",
    lore="The AK-104S, integrated into the CCC5 Combat Compression Suit, combines battlefield efficiency with devastating firepower. Mounted directly to the forearm and shoulder, the weapon draws from an internal ammo pack located near the suit's O2 tanks. While reliable, the ammo pack is a critical weakness—if destroyed, it can ignite and trigger a catastrophic explosion.",
    bonus=0,
    damage=2,
    range="Long",
    weight=None,
    cost=0,
    weapon_class="rifle",
    damage_type="ballistic",
    full_auto=True,
    armor_effect="armor_piercing",
    integrated_in="CCC5 Combat Compression Suit",
    vulnerable_component="Ammo pack (–2 to hit; if destroyed, triggers Blast Power 9 explosion and destroys suit)"
)

rmc_f903we_automatic_assault_rifle = WeaponItem(
    name="RMC F903WE Automatic Assault Rifle",
    lore="A century-old design, the F903WE served in Weyland-Yutani's early colonization efforts and now sees widespread use among colonial militias and mercenaries. Though not a pulse weapon and limited in armor penetration, its reliability and raw firepower make it a trusted choice in frontier conflicts.",
    bonus=0,
    damage=2,
    range="Long",
    weight=2,
    cost=500,
    weapon_class="rifle",
    damage_type="ballistic",
    full_auto=True
)

weyland_yutani_nsg23_assault_rifle = WeaponItem(
    name="Weyland-Yutani NSG23 Assault Rifle",
    lore="A next-generation replacement for the old Storm Rifle, the NSG23 combines a high-capacity drum with an underbarrel ID23 incinerator. Favored by the 3WE Royal Space Marines and Weyland-Yutani security forces, it was passed over by the USCMC in favor of more armor-piercing options.",
    bonus=2,
    damage=2,
    range="Long",
    weight=1,
    cost=1500,
    weapon_class="rifle",
    damage_type="ballistic",
    full_auto=True,
    secondary_weapon="ID23 Incinerator Unit"
)

weyland_yutani_id23_underbarrel_incinerator_unit = WeaponItem(
    name="Weyland-Yutani ID23 Underbarrel Incinerator Unit",
    lore="Compact and deadly, the ID23 is designed to attach beneath an assault rifle, providing infantry with immediate incendiary capability. Though it has limited range and fuel compared to full-sized flamethrowers, it delivers intense fire that can quickly turn the tide in close quarters combat.",
    bonus=0,
    damage=2,
    range="Medium",
    weight=None,
    cost=700,
    weapon_class="rifle",
    damage_type="fire",
    fire_intensity=7,
    fire_on_hit=True,
    integrated_in="NSG23 Assault Rifle"
)

weyland_es7_supernova = WeaponItem(
    name="Weyland ES-7 Supernova Dual-Action Electrostatic Shockgun",
    lore="An advanced electrostatic weapon designed by Weyland for high-intensity crowd control. The ES-7 delivers armor-piercing rounds charged with a debilitating shock effect. Its versatility allows it to accept standard shotgun ammunition, automatically inflicting a stun effect on impact.",
    bonus=2,
    damage=2,
    range="Short",
    weight=1,
    cost=1200,
    weapon_class="rifle",
    damage_type="ballistic",
    armor_effect="armor_piercing",
    inflicts_condition="stunned"
)


weyland_storm_rifle = WeaponItem(
    name="Weyland Storm Rifle",
    lore="Originally designed as a high-end showcase weapon, the Weyland Storm Rifle featured cutting-edge targeting systems and exceptional range. Though never intended for mass deployment, a clerical error led to widespread distribution during colonial peacekeeping efforts. Its legacy lives on in the design of more modern rifles.",
    bonus=1,
    damage=2,
    range="Extreme",
    weight=2,
    cost=3000,
    weapon_class="rifle",
    damage_type="ballistic",
    armor_effect="armor_piercing",
    full_auto=True,
    secondary_weapon="Underbarrel Shotgun"
)

# === HEAVY WEAPONS ===

armat_u1_grenade_launcher = WeaponItem(
    name="Armat U1 Grenade Launcher",
    lore="A 30mm pump-action grenade launcher, often integrated with the M41A Pulse Rifle but also used standalone. The U1 accommodates a variety of grenade types, including high explosive, smoke, and flash grenades, and is known for its versatility against multiple threats.",
    bonus=1,
    damage=1,  # +1 damage to direct target (per rulebook)
    range="Long",
    weight=0.5,
    cost=600,
    weapon_class="heavy",
    damage_type="blast",
    uses_ammo=True,
    blast_power=9,
    ammo_types=["high explosive", "smoke", "flash", "electroshock"],
    special_effect="can_fire_various_grenades"
)

armat_m41ae2_heavy_pulse_rifle = WeaponItem(
    name="Armat M41AE2 Heavy Pulse Rifle",
    lore="A Squad Automatic Weapon modification of the M41A Pulse Rifle, the M41AE2 features a longer barrel in place of the U1 grenade launcher. Designed for suppressive fire and superior battlefield control, it is the USCMC’s go-to support rifle.",
    bonus=1,
    damage=3,
    range="Extreme",
    weight=2,
    cost=1500,
    weapon_class="heavy",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing",
    full_auto=True
)

m56a2_smart_gun = WeaponItem(
    name="M56A2 Smart Gun",
    lore="The heavy firepower backbone of every USCMC squad, the M56A2 Smart Gun is mounted on an articulating arm and gimbal attached to an armored harness. Featuring infrared tracking and a Head Mounted Sight interface, it automatically identifies threats while leaving fire control to the user. Capable of bursts or full auto fire, it is devastating on the battlefield.",
    bonus=3,
    damage=3,
    range="Long",
    weight=3,
    cost=6000,
    weapon_class="heavy",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing",
    full_auto=True
)

m240_incinerator_unit = WeaponItem(
    name="M240 Incinerator Unit",
    lore="A carbine-style flamethrower using naphtha fuel canisters to fire a thick, steady stream of flame at targets. Commonly used by USCMC squads and fireteams, the weapon is notorious for its ability to clear hostile organisms and has earned the field nickname 'Bake-a-Flake.' Targets hit by the incinerator catch fire, making it especially deadly in close encounters.",
    bonus=0,
    damage=2,
    range="Medium",
    weight=1,
    cost=500,
    weapon_class="heavy",
    damage_type="fire",
    uses_ammo=True,
    fire_intensity=9,
    fire_on_hit=True
)

ua_571c_sentry_gun = WeaponItem(
    name="UA 571-C Automated Sentry Gun",
    lore="Tripod-mounted and fully automated, the UA 571-C Sentry Gun forms an autonomous perimeter defense system. Equipped with thermal and motion-tracking AI, it can identify and engage targets without human oversight. While Advanced Recognition Software helps avoid friendly fire, default settings will engage anything that moves and generates heat. Fires with RANGED COMBAT 8 when in autonomous overwatch mode.",
    bonus=2,
    damage=4,
    range="Extreme",
    weight=None,  # Too large/heavy to carry
    cost=12000,
    weapon_class="heavy",
    damage_type="ballistic",
    uses_ammo=True,
    armor_effect="armor_piercing",
    full_auto=True,
    autonomous=True,
    autonomous_skill=8
)

armat_u4a2_repeating_grenade_launcher = WeaponItem(
    name="Armat U4A2 Repeating Grenade Launcher",
    lore="Originally designed for CBRN sterilization teams, the U4A2 offers rapid-fire grenade launching capabilities. While typically loaded with U4 QTC firebombs, it can be equipped with a variety of grenades for different mission profiles, providing versatile area suppression and hazard deployment.",
    bonus=2,
    damage=0,
    range="Long",
    weight=2,
    cost=1100,
    weapon_class="heavy",
    damage_type="blast",
    ammo_types=["frag", "smoke", "flash", "electroshock", "firebomb"],
    uses_ammo=True
)

m5a3_rpg_launcher = WeaponItem(
    name="M5A3 RPG Launcher",
    lore="Equipped with a telescopic sight, this shoulder-fired rocket launcher delivers high-powered explosive payloads with precision. Its armor-piercing warheads make it the ideal anti-vehicle or bunker busting solution, though it requires reloading after every shot.",
    bonus=1,
    damage=5,
    range="Extreme",
    weight=2,
    cost=1800,
    weapon_class="heavy",
    damage_type="blast",
    single_shot=True,
    armor_effect="armor_piercing"
)

norcomm_rpg122 = WeaponItem(
    name="Norcomm RPG122",
    lore="A utilitarian and cost-effective rocket launcher, the RPG122 dispenses with advanced optics in favor of simplicity and durability. Though crude, its armor-piercing warheads remain effective against vehicles and fortifications alike.",
    bonus=0,
    damage=5,
    range="Extreme",
    weight=2,
    cost=1700,
    weapon_class="heavy",
    damage_type="blast",
    single_shot=True,
    armor_effect="armor_piercing"
)

weyland_72a_lew = WeaponItem(
    name="Weyland 72A Light Energy Weapon",
    lore="This shoulder-mounted directed energy cannon is powered by a 15mW pack and fires vaporized cadmium telluride pellets. Originally deployed for ship defense and ground support, its devastating short-range punch is tempered by its cumbersome nature and delayed recharge cycle.",
    bonus=1,
    damage=6,
    range="Extreme",
    weight=3,
    cost=10500,
    weapon_class="heavy",
    damage_type="energy",
    armor_effect="armor_piercing",
    range_damage_falloff="-1 damage per range band beyond Short",
    recharge_time="2 rounds between firing"
)

m78_pig = WeaponItem(
    name="M78 PIG Phased-Plasma Infantry Gun",
    lore="A USCMC-issued phased-plasma gun that delivers heavy energy payloads on target. Though less favored than traditional rockets, the M78 PIG sees use in extreme environments and specialized infantry divisions.",
    bonus=1,
    damage=6,
    range="Extreme",
    weight=3,
    cost=9000,
    weapon_class="heavy",
    damage_type="energy",
    armor_effect="armor_piercing",
    range_damage_falloff="-1 damage per range band beyond Short"
)

ua_102_20_phalanx = WeaponItem(
    name="UA-102-20 Particle Beam Phalanx",
    lore="This illegal, vehicle-mounted CIWS consists of twenty particle beams operating in unison. Designed to defend against overwhelming force, it can fire automatically or shift into a devastating single-target focused mode. Overload attempts may lead to catastrophic detonation.",
    bonus=2,
    damage=4,
    max_damage=7,
    range="Long",
    alternate_fire_mode="Focused fire: +3 damage, Extreme range, no full auto",
    weight=None,
    cost=25000,
    weapon_class="heavy",
    damage_type="energy",
    armor_effect="armor_piercing",
    full_auto=True,
    recharge_time="2 rounds between firing",
    overload_risk="On forced fire, roll Stress Die. On 1, explode (Blast 12)",
    autonomous=True
)

rexim_rxf_m4_eva_mining_laser = WeaponItem(
    name="Rexim RXF-M4 EVA Mining Laser",
    lore="Originally intended for asteroid and hull mining, the RXF-M4 was repurposed by rebel miners during the 2106 Torin Prime uprising. Its intense cutting beam made it a brutal improvised weapon.",
    bonus=-2,
    damage=3,
    range="Short",
    weight=2,
    cost=400,
    weapon_class="heavy",
    damage_type="energy",
    armor_effect="armor_piercing",
    power_supply=5
)

weyland_flammenmacher_3 = WeaponItem(
    name="Weyland Flammenmacher 3 Heavy Incinerator Unit",
    lore="An older industrial flamethrower once used for sanitation and forestry, the Flammenmacher 3 has found renewed utility on the Frontier for crowd suppression and xenobiological threats.",
    bonus=1,
    damage=3,
    range="Long",
    weight=2,
    cost=2000,
    weapon_class="heavy",
    damage_type="fire",
    fire_intensity=12,
    fire_on_hit=True
)

# === DEPLOYABLES ===

g2_electroshock_grenade = WeaponItem(
    name="G2 Electroshock Grenade",
    lore="Nicknamed 'electronic ballbreakers,' these grenades self-propel before releasing a powerful electric pulse capable of stunning anyone in the blast zone. Targets must make a hard STAMINA roll (-2) or be stunned for one round. Popular for crowd control or desperate last stands.",
    bonus=0,
    damage=0,
    range="Medium",
    weight=0.5,
    cost=400,
    weapon_class="grenade",
    damage_type="stun",
    uses_ammo=False,
    special_effect="Stun (STAMINA -2, lose slow action for 1 round)"
)

hedp_grenade_m40 = WeaponItem(
    name="Armat M40 HEDP Grenade",
    lore="A standard high-explosive dual-purpose grenade compatible with U1 and U4 launchers. Common among USCMC units and adaptable for hand-throwing with minor preparation.",
    bonus=0,
    damage_type="blast",
    blast_power=9,
    range="Medium",
    weight=0.25,
    cost=60,
    weapon_class="grenade",
    special_effect="Can be used with launchers or as hand grenade"
)

m72a1_starshell_flare = WeaponItem(
    name="M72A1 Starshell Flare",
    lore="A 30mm illumination round used in grenade launchers. When fired skyward, it brightly illuminates an entire combat zone for several rounds, aiding visibility in low-light operations.",
    bonus=0,
    damage=2,
    range="Medium",
    weight=0.25,
    cost=50,
    weapon_class="grenade",
    damage_type="physical",
    special_effect="Illuminates one zone",
    critical_override="#15 if direct hit"
)

m230_baton_round = WeaponItem(
    name="M230 Baton Round",
    lore="Non-lethal rubber projectiles used in urban crowd control. Favored for their ability to incapacitate without killing, these rounds are common issue for U1 and U4 grenade launchers.",
    bonus=0,
    damage=3,
    range="Short",
    weight=0.25,
    cost=30,
    weapon_class="launcher",
    damage_type="impact",
    ammo_types=["U1", "U4"],
    armor_effect="armor_doubled",
    critical_override="random: #16, #24, #33"
)

m108_buckshot_canister = WeaponItem(
    name="M108 Buckshot Canister",
    lore="Oversized shotgun shells for use in U1 and U4 grenade launchers, delivering a powerful short-range spread. Frequently employed by Colonial Marshals on remote colonies.",
    bonus=0,
    damage=3,
    range="Short",
    weight=0.25,
    cost=30,
    weapon_class="launcher",
    damage_type="kinetic",
    ammo_types=["U1", "U4"],
    armor_effect="armor_doubled"
)

u4_qtc_firebomb_ammunition = WeaponItem(
    name="U4 QTC Firebomb Ammunition",
    lore="Loaded with quinitricetyline for decontamination and crowd suppression, this round incinerates entire zones on impact. Designed for use in U1 and U4 grenade launchers.",
    bonus=0,
    damage=0,
    range="Medium",
    weight=0.25,
    cost=600,
    weapon_class="launcher",
    damage_type="fire",
    fire_intensity=12,
    ammo_types=["U1", "U4"],
    area_effect="incinerates target zone"
)

armat_type_4_assault_breaching_charge = WeaponItem(
    name="Armat Type 4 Assault Breaching Charge",
    lore="A focused, adhesive explosive charge used for breaching sealed doors or reinforced walls. Detonated by timer or remote, and highly effective at close range.",
    bonus=0,
    damage=0,
    range="Engaged",
    weight=1,
    cost=200,
    weapon_class="explosive",
    damage_type="blast",
    blast_power=9,
    armor_effect="armor_piercing",
    special_effect="damage +2 to immediate target"
)

m20_claymore_mine = WeaponItem(
    name="M20 Claymore Mine",
    lore="A proximity-triggered anti-personnel mine equipped with a laser tripwire. Designed for area denial and ambush scenarios, it requires a keen eye to detect before detonation.",
    bonus=0,
    damage=0,
    range="Short",
    weight=0.5,
    cost=150,
    weapon_class="explosive",
    damage_type="blast",
    blast_power=9,
    detonation_trigger="proximity",
    special_effect="requires Observation roll to detect"
)

m111_anti_vehicle_mine = WeaponItem(
    name="M111 Anti-Vehicle Mine",
    lore="A pressure-sensitive explosive device designed to disable both personnel and vehicles. Triggered by weight at close range, it delivers a devastating payload capable of breaching heavy armor.",
    bonus=0,
    damage=0,
    range="Engaged",
    weight=2,
    cost=1000,
    weapon_class="explosive",
    damage_type="blast",
    blast_power=12,
    detonation_trigger="pressure",
    special_effect="Damage +2 vs immediate target, armor piercing"
)

cn20_nerve_agent_canister = WeaponItem(
    name="CN-20 Nerve Agent Canister",
    lore="A banned chemical weapon outside Earth, CN-20 is deployed in warzones on the Frontier to incapacitate entire zones of enemy personnel. Victims without hazmat protection quickly succumb to convulsions and death unless treated.",
    bonus=0,
    damage=0,
    range="Zone",
    weight=1,
    cost=1000,
    weapon_class="chemical",
    damage_type="special",
    area_effect="All humans in zone",
    inflicts_condition="nerve_agent_effects",
    persistent_effect="Roll Stress Die each round to see if gas dissipates"
)

qtc_explosive_accelerant = WeaponItem(
    name="QTC Quinitricetyline Explosive Accelerant",
    lore="A volatile and toxic chemical similar to napalm, QTC is used to incinerate entrenched enemies, hostile wildlife, or infectious outbreaks. Often deployed in bulk, a single drum can devastate entire structures.",
    bonus=0,
    damage=0,
    range="Zone",
    weight=1,
    cost=200,  # Per liter
    weapon_class="chemical",
    damage_type="fire",
    fire_intensity=15,
    area_effect="Incinerates all targets in zone",
    persistent_effect="Fire spreads and intensifies if not contained"
)

kip_baton_round = WeaponItem(
    name="KIP Baton Round",
    lore="Non-lethal rubber rounds issued to Colonial Marshals for crowd control. Effective at incapacitating without permanent harm.",
    bonus=0,
    damage=2,
    range="Short",
    weight=None,
    cost=30,
    weapon_class="ammunition",
    damage_type="impact",
    armor_effect="armor_doubled",
    critical_override="#16, #24, or #33",
    special_ammo_effect="usable in shotgun or shockgun"
)

wildcatter_b9_blast_mining_charge = WeaponItem(
    name="Wildcatter B9 Blast-Mining Charge",
    lore="Designed for industrial excavation, the B9 is frequently used in field demolitions. It can also be weaponized to devastating effect.",
    bonus=0,
    damage=0,
    blast_power=9,
    range="Short",
    weight=1,
    cost=200,
    weapon_class="explosive",
    damage_type="blast",
    armor_effect="armor_piercing",
    direct_target_bonus="+2 damage to direct target",
    detonation_trigger="timer or remote"
)

# === MELEE ===

stun_baton = WeaponItem(
    name="Stun Baton",
    lore="An electroshock device often used for controlling pests and livestock. While non-lethal, a solid hit can incapacitate a human target. Anyone struck and taking damage must make a STAMINA roll or be stunned for one round. Requires a Power Supply roll after each use.",
    bonus=1,
    damage=1,
    range="Engaged",
    weight=0.5,
    cost=80,
    weapon_class="melee",
    damage_type="stun",
    uses_ammo=True,
    power_supply=5,
    special_effect="Stun on hit (STAMINA roll or stunned for 1 round)"
)

mechanical_cutting_torch = WeaponItem(
    name="Mechanical Cutting Torch",
    lore="A utilitarian blowtorch primarily used for welding and cutting through metal, though it can serve as an improvised melee weapon in a pinch. A relic of practicality, the torch must make a Power Supply roll after each use.",
    bonus=0,
    damage=3,
    range="Engaged",
    weight=1,
    cost=300,
    weapon_class="melee",
    damage_type="energy",
    uses_ammo=True,
    power_supply=5,
    armor_effect="armor_piercing"
)

unarmed_attack = WeaponItem(
    name="Unarmed Attack",
    lore="Nothing fancy—just fists, elbows, knees, or any part of the body that works in a desperate situation. Fighting barehanded is risky, especially against armed or armored foes, but sometimes it’s all you’ve got.",
    bonus=0,
    damage=1,
    range="Engaged",
    weight=None,
    cost=0,
    weapon_class="melee",
    damage_type="blunt",
    armor_effect="armor_doubled"
)

blunt_instrument = WeaponItem(
    name="Blunt Instrument",
    lore="A pipe, wrench, crowbar, or anything heavy and solid enough to swing. In desperate or improvised combat, blunt objects become brutal close-range weapons capable of cracking skulls and breaking bones.",
    bonus=1,
    damage=1,
    range="Engaged",
    weight=1,
    cost=0,
    weapon_class="melee",
    damage_type="blunt"
)

knife = WeaponItem(
    name="Knife",
    lore="A basic combat knife or utility blade. Favored by scouts, engineers, and survivors alike, knives are light, versatile, and deadly in skilled hands—especially up close.",
    bonus=0,
    damage=2,
    range="Engaged",
    weight=0.5,
    cost=50,
    weapon_class="melee",
    damage_type="piercing"
)

