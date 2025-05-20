import discord                          # type: ignore
from discord.ext import commands        # type: ignore
from discord import app_commands        # type: ignore
from discord.ui import View, Button     # type: ignore
import json
import os
import asyncio
from dotenv import load_dotenv
from typing import Dict, Optional, Tuple
from models.character import Character, Attributes, Skills
from models.items import Item, ConsumableItem, Inventory
from models.dice import DiceRoll
import datetime
import re
import copy  # Add at the top with other imports
import logging
from models.wearables import all_wearable_items
from models.weapons import all_weapon_items  # You may need to create this list in weapons.py if not present
from models.wearables import WearableLoadout
from models.weapon_item import WeaponItem
from character_creation.utils import (
    format_attribute_bar, format_skill_bar, get_paired_gear, get_article_for_item, find_wearable_by_name, find_weapon_by_name, handle_dice_roll_item,
    get_skill_and_attr, get_type_icon, get_ammo_icon, get_modifiers
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import datetime

def log_debug(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug(f"{ts} | {msg}")

# Load environment variables
load_dotenv()

# ==============================
# Alien RPG Discord Bot — FINAL GLOBAL
# ==============================
# comment

LOG_PATH = os.path.join(os.path.dirname(__file__), "scripts", "bot.log")

def log_event(msg: str):
    with open(LOG_PATH, "a") as f:
        ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{ts} [EVENT   ] {msg}\n")

# DataManager and related logic moved to data_manager.py
from data_manager import data_manager

# Session management moved to character_creation/session.py
from character_creation.session import creation_sessions

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("[OK] SYSTEM ONLINE")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

# DEBUG LOGGING SETUP
DEBUG_LOG_PATH = os.path.join(os.path.dirname(__file__), "debug.log")

def debug_log(msg: str, sender: str = None, user: str = None):
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    if sender and user:
        with open(DEBUG_LOG_PATH, "a") as f:
            f.write(f"{ts} | {sender} | {user}\n{msg}\n{'-'*60}\n")
    else:
        with open(DEBUG_LOG_PATH, "a") as f:
            f.write(f"{ts} | {msg}\n{'-'*60}\n")

# Purge debug log on bot start
with open(DEBUG_LOG_PATH, "w") as f:
    f.write("")

# --- PATCH send_dm to log all bot outputs ---
async def send_dm(user, content, view=None):
    try:
        debug_log(content, sender="BOT", user=str(user))
        return await user.send(content, view=view)
    except discord.Forbidden:
        return None

# --- PATCH all user input to log responses ---
async def wait_for_user_message(user, *args, **kwargs):
    def check(m):
        return m.author.id == user.id and isinstance(m.channel, discord.DMChannel)
    
    try:
        msg = await bot.wait_for("message", check=check, *args, **kwargs)
        debug_log(msg.content, sender="USER", user=str(user))
        return msg
    except Exception as e:
        logger.error(f"Error waiting for user message: {e}")
        raise

from character_creation.steps import (
    select_personal_details, select_career, start_attr, assign_skills, select_talent, select_agenda, select_gear, select_signature_item, apply_starting_cash_and_finalize, finalize_character, edit_section
)

from character_creation.utils import (
    format_attribute_bar, format_skill_bar, get_paired_gear, get_article_for_item, find_wearable_by_name, find_weapon_by_name, handle_dice_roll_item,
    get_skill_and_attr, get_type_icon, get_ammo_icon, get_modifiers
)

async def start_attr(user, char_id: str):
    user_id = str(user.id)
    careers = data_manager.get_playergen()["Careers"]
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found – start with /createcharacter.\n```")
        return
    char = creation_sessions[user_id][char_id]
    key_attr = careers[char.career]["key_attribute"]
    attr_order = ["Strength", "Agility", "Wits", "Empathy"]
    points_remaining = 6
    current_attr_index = 0
    manual_nav = False
    while True:
        current_attr = attr_order[current_attr_index]
        display = [
            "```text",
            ">> Attribute Allocation <<\n"
        ]
        if points_remaining == 6:
            display.extend([
                f"As a {char.career}, your key attribute is {key_attr} (max 5)",
                "• Minimum for any attribute is 2",
                "• Other attribute max: 4",
                "• All points must be allocated\n"
            ])
        display.append(f"Points remaining: {points_remaining}")
        display.append("==========================")
        for attr in attr_order:
            value = getattr(char.attributes, attr.lower())
            is_key = attr == key_attr
            bar = format_attribute_bar(value, is_key)
            pointer = " <<< Add points (0-{})".format(
                min(points_remaining, (5 if is_key else 4) - value)
            ) if attr == current_attr and (not (value == (5 if is_key else 4))) and points_remaining > 0 else ""
            display.append(f"{attr:<8}  {value} {bar}{pointer}")
        other_attrs = [a for a in attr_order if a != current_attr]
        display.append("\nEnter letter to edit: " + ", ".join(f"({a[0]}){a[1:]}" for a in other_attrs))
        display.append("Enter R to reset value.")
        value = getattr(char.attributes, current_attr.lower())
        is_key = current_attr == key_attr
        max_add = min(points_remaining, (5 if is_key else 4) - value)
        if (points_remaining > 0) and (not (value == (5 if is_key else 4)) or manual_nav):
            display.append(f"Enter a number to add to {current_attr} (0-{max_add}),\nor enter 4 numbers to assign all values at once (e.g. 4, 2, 4, 4)")
        if points_remaining > 0:
            if points_remaining == 1:
                display.append(f"\nYou have 1 point left to allocate.")
            else:
                display.append(f"\nYou have {points_remaining} points left to allocate.")
        display.append("```")
        # If all points are allocated, skip input and go to confirmation
        if points_remaining == 0:
            while True:
                display = ["```text", ">> Final Attribute Allocation <<\n"]
                display.append("==========================")
                for attr in attr_order:
                    value = getattr(char.attributes, attr.lower())
                    is_key = attr == key_attr
                    bar = format_attribute_bar(value, is_key)
                    display.append(f"{attr:<8}  {value} {bar}")
                display.append("\nConfirm allocation? (Y/N)```")
                await send_dm(user, "\n".join(display))
                confirm = await wait_for_user_message(user)
                if confirm.content.strip().upper() == "Y":
                    await send_dm(user, "```text\n[OK] Attributes saved. Proceeding to Skills...\n```")
                    await assign_skills(user_id, char_id)
                    return
                elif confirm.content.strip().upper() == "N":
                    await send_dm(user, """```text\n[RESET] Let's enter the values again.\n```""")
                    # Reset all to 2
                    for attr in attr_order:
                        setattr(char.attributes, attr.lower(), 2)
                    points_remaining = 6
                    current_attr_index = 0
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Please enter Y or N\n```")
                    continue
            continue  # skip rest of loop
        await send_dm(user, "\n".join(display))
        msg = await wait_for_user_message(user)
        cmd = msg.content.strip().upper()
        vals = None
        manual_nav = False
        multi_match = re.match(r"^(\d+)[,\s]+(\d+)[,\s]+(\d+)[,\s]+(\d+)$", cmd)
        if multi_match:
            vals = [int(multi_match.group(i)) for i in range(1, 5)]
        elif re.match(r"^\d{4}$", cmd):
            vals = [int(x) for x in cmd]
        if vals:
            min_vals = [2, 2, 2, 2]
            max_vals = [5 if attr == key_attr else 4 for attr in attr_order]
            total_points = sum([v - 2 for v in vals])
            if any(vals[i] < min_vals[i] or vals[i] > max_vals[i] for i in range(4)):
                await send_dm(user, f"```text\n[ERROR] Invalid allocation. Each attribute must be in range (key: 2-5, others: 2-4).\n```")
                continue
            if total_points > 6:
                await send_dm(user, f"```text\n[ERROR] You used more than 6 points.\n```")
                continue
            for i, attr in enumerate(attr_order):
                setattr(char.attributes, attr.lower(), vals[i])
            points_remaining = 6 - total_points
            if points_remaining > 0:
                for i, attr in enumerate(attr_order):
                    value = getattr(char.attributes, attr.lower())
                    is_key = attr == key_attr
                    if value < (5 if is_key else 4):
                        current_attr_index = i
                        break
                continue 
        elif cmd == "R":
            current_value = getattr(char.attributes, current_attr.lower())
            if current_value > 2:
                points_remaining += current_value - 2
                setattr(char.attributes, current_attr.lower(), 2)
            continue
        elif cmd in ["S", "A", "W", "E"]:
            attr_map = {"S": "Strength", "A": "Agility", "W": "Wits", "E": "Empathy"}
            if attr_map[cmd] != current_attr:
                current_attr_index = attr_order.index(attr_map[cmd])
                manual_nav = True
            continue
        elif cmd.isdigit():
            points = int(cmd)
            value = getattr(char.attributes, current_attr.lower())
            is_key = current_attr == key_attr
            max_add = min(points_remaining, (5 if is_key else 4) - value)
            if points < 0 or points > max_add:
                await send_dm(user, f"```text\n[ERROR] Please enter a number between 0 and {max_add}\n```")
                continue
            setattr(char.attributes, current_attr.lower(), value + points)
            points_remaining -= points
            # Move pointer to next attribute that can accept points
            for i in range(len(attr_order)):
                idx = (current_attr_index + 1 + i) % len(attr_order)
                value = getattr(char.attributes, attr_order[idx].lower())
                is_key = attr_order[idx] == key_attr
                if value < (5 if is_key else 4):
                    current_attr_index = idx
                    break
            continue
        else:
            await send_dm(user, "```text\n[ERROR] Please enter a valid command\n```")
            continue

async def assign_skills(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
    char = creation_sessions[user_id][char_id]
    key_skills = careers[char.career]["key_skills"]
    all_skills = list(data_manager.get_playergen()["Skills"].keys())
    points_remaining = 10
    current_skill_index = 0
    manual_nav = False
    while True:
        display = ["```text", ">> Key Skill Allocation <<\n"]
        display.append(f"Points remaining: {points_remaining}")
        display.append("==========================")
        for i, skill in enumerate(key_skills):
            skill_attr = skill.lower().replace(" ", "_")
            value = getattr(char.skills, skill_attr)
            pointer = " <<< Add points (0-{})".format(
                min(points_remaining, 3 - value)
            ) if i == current_skill_index and (not (value == 3)) else ""
            display.append(f"[{i+1}] {skill:<15} {value} {format_skill_bar(value)}{pointer}")
        display.append("\nFor each skill point remaining, you will be allowed an additional skill at the next step.")
        display.append("Enter a number to add to the current skill, or enter 3 numbers to assign all points at once.")
        display.append("N proceeds to general skill selection, R resets these key skills.")
        display.append("```")
        await send_dm(user, "\n".join(display))
        msg = await wait_for_user_message(user)
        cmd = msg.content.strip().upper()
        vals = None
        manual_nav = False
        multi_match = re.match(r"^(\d+)[,\s]+(\d+)[,\s]+(\d+)$", cmd)
        if multi_match:
            vals = [int(multi_match.group(i)) for i in range(1, 4)]
        elif re.match(r"^\d{3}$", cmd):
            vals = [int(x) for x in cmd]
        if vals:
            if any(v < 0 or v > 3 for v in vals):
                await send_dm(user, "```text\n[ERROR] Each key skill must be 0-3.\n```")
                continue
            if sum(vals) > points_remaining:
                await send_dm(user, f"```text\n[ERROR] Total points exceed available ({points_remaining}).\n```")
                continue
            for i, skill in enumerate(key_skills):
                skill_attr = skill.lower().replace(" ", "_")
                setattr(char.skills, skill_attr, vals[i])
            points_remaining = 10 - sum(vals)
            # If all points assigned or multi-assignment, break to general skills immediately
            break
        elif cmd == "R":
            for skill in key_skills:
                skill_attr = skill.lower().replace(" ", "_")
                points_remaining += getattr(char.skills, skill_attr)
                setattr(char.skills, skill_attr, 0)
            current_skill_index = 0
            continue
        elif cmd == "N" or cmd == "NEXT":
            break
        elif cmd.isdigit():
            pts = int(cmd)
            skill = key_skills[current_skill_index]
            skill_attr = skill.lower().replace(" ", "_")
            value = getattr(char.skills, skill_attr)
            max_add = min(points_remaining, 3 - value)
            if pts < 0 or pts > max_add:
                await send_dm(user, f"```text\n[ERROR] Must be 0-{max_add}.\n```")
                continue
            setattr(char.skills, skill_attr, value + pts)
            points_remaining -= pts
            # Move pointer to next skill that can accept points
            for i in range(len(key_skills)):
                idx2 = (current_skill_index + 1 + i) % len(key_skills)
                value2 = getattr(char.skills, key_skills[idx2].lower().replace(" ", "_"))
                if value2 < 3:
                    current_skill_index = idx2
                    break
            continue
        else:
            await send_dm(user, "```text\n[ERROR] Enter three numbers (0-3) for key skills, a number to add to the current skill, N to proceed, or R to reset.\n```")
            continue
    # --- General Skills Multi-Entry ---
    available_skills = [s for s in all_skills if s not in key_skills]
    while True:
        skill_list = '\n'.join(f"[{i+1}] {s}" for i, s in enumerate(available_skills) if getattr(char.skills, s.lower().replace(" ", "_")) == 0)
        await send_dm(user, f"""```text\nEnter general skills to assign (comma/space-separated indices, up to {points_remaining}):\nType B to go back to key skills.\n{skill_list}\n```""")
        if points_remaining <= 0:
            break
        msg = await wait_for_user_message(user)
        cmd = msg.content.strip().upper()
        if cmd == "B" or cmd == "BACK":
            # Go back to key skills
            await assign_skills(user_id, char_id)
            return
        indices = re.findall(r"\d+", cmd)
        if indices:
            indices = [int(i)-1 for i in indices]
            if any(i < 0 or i >= len(available_skills) for i in indices):
                await send_dm(user, f"```text\n[ERROR] Invalid skill index.\n```")
                continue
            if len(indices) > points_remaining:
                await send_dm(user, f"```text\n[ERROR] You selected more skills than you have points ({points_remaining}).\n```")
                continue
            # If only one index, assign one point and re-prompt with feedback and updated list
            if len(indices) == 1:
                skill = available_skills[indices[0]]
                skill_attr = skill.lower().replace(" ", "_")
                if getattr(char.skills, skill_attr) > 0:
                    await send_dm(user, f"```text\n[ERROR] You have already assigned a point to {skill}.\n```")
                    continue
                setattr(char.skills, skill_attr, 1)
                points_remaining -= 1
                if points_remaining > 0:
                    await send_dm(user, f"```text\n[OK] Selected {skill}. You can make {points_remaining} more selection{'s' if points_remaining != 1 else ''}.\n```")
                    continue
                break
            # Otherwise, assign one point to each selected skill (batch)
            for i in indices[:points_remaining]:
                skill = available_skills[i]
                skill_attr = skill.lower().replace(" ", "_")
                if getattr(char.skills, skill_attr) > 0:
                    await send_dm(user, f"```text\n[ERROR] You have already assigned a point to {skill}.\n```")
                    continue
                setattr(char.skills, skill_attr, 1)
            points_remaining -= min(len(indices), points_remaining)
            break
        elif cmd.upper() == "X":
            break
        else:
            await send_dm(user, "```text\n[ERROR] Enter skill indices separated by commas or spaces, B to go back, or X to finish.\n```")
            continue
    # Final confirmation
    display = ["```text", ">> Final Skill Allocation <<\n"]
    display.append("==========================")
    display.append("Key Skills:")
    for skill in key_skills:
        skill_attr = skill.lower().replace(" ", "_")
        value = getattr(char.skills, skill_attr)
        display.append(f"{skill:<15} {value} {format_skill_bar(value)}")
    general_skills = [s for s in all_skills if s not in key_skills and getattr(char.skills, s.lower().replace(" ", "_")) > 0]
    if general_skills:
        for skill in general_skills:
            skill_attr = skill.lower().replace(" ", "_")
            value = getattr(char.skills, skill_attr)
            display.append(f"{skill:<15} {value} {format_skill_bar(value)}")
    display.append("\nConfirm allocation? (Y/N)")
    display.append("```")
    await send_dm(user, "\n".join(display))
    confirm = await wait_for_user_message(user)
    if confirm.content.strip().upper() == "Y":
        await send_dm(user, "```text\n[OK] Skills saved. Proceeding to Talent...\n```")
        await select_talent(user_id, char_id)
        return
    else:
        await send_dm(user, "```text\n[RESET] Let's reassign skills.\n```")
        # Reset all skills
        for skill in key_skills + available_skills:
            skill_attr = skill.lower().replace(" ", "_")
            setattr(char.skills, skill_attr, 0)
        await assign_skills(user_id, char_id)
        return

async def select_talent(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    playergen = data_manager.get_playergen()
    careers = playergen["Careers"]
    talents = playergen["Talents"]
    
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id][char_id]
    career_talents = careers[char.career]["talents"]
    
    menu = ["```text", ">> TALENT SELECTION <<"]
    menu.append(f"Select a talent for your {char.career}:")
    menu.append("\nAvailable talents:")
    
    for i, talent_name in enumerate(career_talents, 1):
        description = ""
        if char.career in talents and talent_name in talents[char.career]:
            description = talents[char.career][talent_name]["description"]
        elif "General" in talents and talent_name in talents["General"]:
            description = talents["General"][talent_name]["description"]
        
        menu.append(f"[{i}] {talent_name}")
        menu.append(f"   {description}")
        menu.append("")
        
    menu.append("\nEnter the number of your chosen talent:```")
    
    while True:
        await send_dm(user, '\n'.join(menu))
        msg = await wait_for_user_message(user)
        
        if not msg.content.isdigit():
            await send_dm(user, "```text\n[ERROR] Please enter a number\n```")
            continue
            
        choice = int(msg.content)
        if choice < 1 or choice > len(career_talents):
            await send_dm(user, f"```text\n[ERROR] Please enter a number between 1 and {len(career_talents)}\n```")
            continue
        
        selected = career_talents[choice - 1]
        char.talent = selected
        await send_dm(user, f"```text\n[OK] Talent saved. Proceeding to Personal Agenda...\n```")
        await select_agenda(user_id, char_id)
        return

async def select_agenda(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id][char_id]
    agendas = careers[char.career]["personal_agendas"]
    
    menu = ["```text", ">> PERSONAL AGENDA <<"]
    menu.append(f"Select a personal agenda for your {char.career}:")
    menu.append("\nAvailable agendas:")
    for i, agenda in enumerate(agendas, 1):
        menu.append(f"[{i}] {agenda}")
    menu.append("\nEnter the number of your chosen agenda:```")
    
    while True:
        await send_dm(user, '\n'.join(menu))
        msg = await wait_for_user_message(user)
        
        if not msg.content.isdigit():
            await send_dm(user, "[ERROR] Please enter a number")
            continue
            
        choice = int(msg.content)
        if choice < 1 or choice > len(agendas):
            await send_dm(user, f"[ERROR] Please enter a number between 1 and {len(agendas)}")
            continue
        
        selected = agendas[choice - 1]
        char.agenda = selected
        await send_dm(user, "[OK] Agenda saved. Proceeding to Gear...")
        await select_gear(user_id, char_id)
        return

def handle_dice_roll_item(item_name: str) -> tuple[str, int]:
    import re
    from models.dice import DiceRoll
    
    dice_pattern = r'(\d+d\d+)\s+(?:doses of|rounds of|)\s*(.+)'
    match = re.match(dice_pattern, item_name)
    
    if match:
        dice_expr, item_name = match.groups()
        quantity = DiceRoll.roll(dice_expr)
        return item_name.strip(), quantity
    return item_name, 1

def get_paired_gear(gear_list: list) -> list[tuple[str, str]]:
    """Identify pairs of mutually exclusive gear items.
    Each career has 8 items organized into 4 pairs."""
    pairs = []
    for i in range(0, len(gear_list), 2):
        if i + 1 < len(gear_list):
            pairs.append((gear_list[i], gear_list[i + 1]))
    return pairs

def get_article_for_item(item_name: str) -> str:
    """Add the appropriate article to an item name based on its characteristics."""
    # Items that should not have any article
    no_article_prefixes = [
        "1d6", "2d6", "3d6", "4d6", "5d6", "6d6",  # Dice rolls
        "1d3", "2d3", "3d3", "4d3", "5d3", "6d3",
        "1d4", "2d4", "3d4", "4d4", "5d4", "6d4",
        "1d8", "2d8", "3d8", "4d8", "5d8", "6d8",
        "1d10", "2d10", "3d10", "4d10", "5d10", "6d10",
        "1d12", "2d12", "3d12", "4d12", "5d12", "6d12",
        "1d20", "2d20", "3d20", "4d20", "5d20", "6d20",
        "1d100", "2d100", "3d100", "4d100", "5d100", "6d100",
        "1 ", "2 ", "3 ", "4 ", "5 ", "6 ",  # Simple quantities
        "1x", "2x", "3x", "4x", "5x", "6x"
    ]
    
    # Check if item starts with any of the no-article prefixes
    for prefix in no_article_prefixes:
        if item_name.startswith(prefix):
            return item_name
    
    # Items that should use "the"
    definite_articles = [
        # Weapons and military equipment
        "M4A3", "M41A", "M56A2", "M314", "M3", "M72", ".357", "Armat",
        "Rexim", "Watatsumi", "B9", "G2", "Model", "Pump-Action",
        # Company/Manufacturer prefixes
        "IRC", "PR-PUT", "Seegson", "Samani", "Daihotai",
        # Personal equipment
        "Personal", "Hand", "Maintenance", "Hi-beam",
        # Plural items that take "the"
        "Binoculars", "Cards", "Drugs", "Pills", "Tools", "Grenades",
        # Other specific items
        "Surgical", "Digital", "Neuro", "Eco", "Recreational"
    ]
    
    # Check if item starts with any of the definite article prefixes
    for prefix in definite_articles:
        if item_name.startswith(prefix):
            return f"the {item_name}"
    
    # Items that should use "an"
    an_prefixes = ["EVA", "IRC", "IFF", "Eco", "Electronic"]
    for prefix in an_prefixes:
        if item_name.startswith(prefix):
            return f"an {item_name}"
    
    # Default to "a" for other items
    return f"a {item_name}"

# --- Helper functions ---
def find_wearable_by_name(name):
    for item in all_wearable_items:
        if item.name.lower() == name.lower():
            return item
    return None

def find_weapon_by_name(name):
    for item in all_weapon_items:
        if item.name.lower() == name.lower():
            return item
    return None

@bot.tree.command(name="createcharacter", description="Begin character creation.")
async def cmd_create(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    
    # Check if user is already in a creation session
    if user_id in creation_sessions and any(session for session in creation_sessions[user_id].values()):
        await interaction.response.send_message(
            "```text\n[ERROR] You already have a character creation session in progress. Please complete or cancel it first.\n```",
            ephemeral=True
        )
        return
    
    user_chars = data_manager.get_user_characters(user_id)
    
    # Generate a unique character ID
    char_id = f"{user.id}_{len(user_chars) + 1}"
    log_debug(f"Start char creation: user {user_id}, char {char_id}")
    
    # Initialize the user's session
    if user_id not in creation_sessions:
        creation_sessions[user_id] = {}
    
    # Clear any existing session for this character
    if char_id in creation_sessions[user_id]:
        del creation_sessions[user_id][char_id]
    
    # Initialize the character in the session with default values
    creation_sessions[user_id][char_id] = Character(
        id=char_id,
        name="",  # Will be set during creation
        career="",  # Will be set during creation
        gender="",
        age=0,
        attributes=Attributes(),
        skills=Skills(),
        talent="",
        agenda="",
        inventory=Inventory(),
        signature_item="",
        cash=0
    )
    
    await interaction.response.send_message(
        "[OK] Check your DMs to begin character creation.",
        ephemeral=True
    )
    
    try:
        await select_personal_details(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
    except Exception as e:
        logger.error(f"Error in character creation: {e}")
        # Clean up the session
        if user_id in creation_sessions and char_id in creation_sessions[user_id]:
            del creation_sessions[user_id][char_id]
        await user.send("```text\n[ERROR] Character creation failed. Please try again with /createcharacter.\n```")

@bot.tree.command(name="sheet", description="View your character sheet.")
async def cmd_sheet(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    log_debug(f"Sheet command by user {user_id}")
    log_debug(f"User {user_id} characters: {[c.name for c in data_manager.get_user_characters(user_id).values()]}")
    log_debug(f"Primary chars: {[data_manager.get_user_characters(uid)[cid].name for uid, cid in data_manager.primary_characters.items() if cid in data_manager.get_user_characters(uid)]}")
    
    char = data_manager.get_primary_character(user_id)
    log_debug(f"Primary char: {char.name if char else 'None'}")
    
    if not char:
        await interaction.response.send_message("```text\n[ERROR] No character sheet found.\n```", ephemeral=True)
        return
        
    sheet = ["```text", ">> CHARACTER SHEET <<"]
    sheet.append(f"\nName: {char.name}")
    sheet.append(f"Career: {char.career}")
    sheet.append("\nAttributes:")
    for attr in ["Strength", "Agility", "Wits", "Empathy"]:
        value = getattr(char.attributes, attr.lower())
        sheet.append(f"  {attr}: {value} {format_attribute_bar(value)}")
    sheet.append("\nSkills:")
    for skill_name, value in char.skills.__dict__.items():
        if value > 0:
            name = skill_name.replace('_', ' ').title()
            sheet.append(f"  {name}: {value} {format_skill_bar(value)}")
    sheet.append(f"\nTalent: {char.talent}")
    sheet.append(f"Personal Agenda: {char.agenda}")
    sheet.append("\nGear:")
    for item in char.inventory.items:
        if isinstance(item, ConsumableItem):
            # Use default values if form/form_plural are not set
            form = getattr(item, 'form', 'unit')
            form_plural = getattr(item, 'form_plural', 'units')
            sheet.append(f"  • {item.name} (x{item.quantity} {form if item.quantity == 1 else form_plural})")
        else:
            sheet.append(f"  • {str(item)}")
    
    sheet.append(f"\nSignature Item: {char.signature_item}")
    sheet.append(f"Cash: ${char.cash}")
    sheet.append("```")
    
    await interaction.response.send_message('\n'.join(sheet), ephemeral=True)

@bot.tree.command(name="deletecharacter", description="Delete a character. Use --force to skip confirmation.")
async def cmd_delete(interaction: discord.Interaction, *, options: str = ""):
    user = interaction.user
    user_id = str(user.id)
    chars = data_manager.get_user_characters(user_id)
    force = "--force" in options.split()
    
    if not chars:
        await interaction.response.send_message("```text\n[ERROR] No characters found.\n```", ephemeral=True)
        return
    
    # Show character list
    char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
    for char_id, char in chars.items():
        is_primary = char_id == data_manager.primary_characters.get(user_id)
        char_list.append(f"{'★ ' if is_primary else ''}{char.name} ({char.career})")
    char_list.append("\nEnter the name of the character you want to delete:")
    char_list.append("```")
    
    await interaction.response.send_message('\n'.join(char_list), ephemeral=True)
    
    def check(m):
        return m.author.id == user.id and isinstance(m.channel, discord.DMChannel)
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        char_name = msg.content.strip()
        
        # Find character by name
        target_char = None
        target_id = None
        for char_id, char in chars.items():
            if char.name.lower() == char_name.lower():
                target_char = char
                target_id = char_id
                break
        
        if not target_char:
            await user.send("```text\n[ERROR] Character not found.\n```")
            return
        
        if target_id == data_manager.primary_characters.get(user_id) and len(chars) > 1:
            await user.send("""```text
This is your primary character. You must set another character as primary before deleting this one.
Use the /characters command to set a different character as primary first.```""")
            return
        
        if not force:
            await user.send(f"""```text
Are you sure you want to delete {target_char.name}?
This action cannot be undone.
Type CONFIRM to proceed.```""")
            
            confirm = await bot.wait_for("message", check=check, timeout=30.0)
            if confirm.content.strip().upper() != "CONFIRM":
                await user.send("```text\n[CANCELLED] Character deletion cancelled.\n```")
                return
        
        if await delete_character(user_id, target_id, interaction.guild):
            await user.send(f"```text\n[OK] {target_char.name} has been deleted.\n```")
        else:
            await user.send("```text\n[ERROR] Failed to delete character.\n```")
            
    except asyncio.TimeoutError:
        await user.send("```text\n[INFO] Command timed out. Use /deletecharacter to start over.\n```")

@bot.tree.command(name="reloaddata", description="Reload all game data from files.")
@app_commands.checks.has_permissions(administrator=True)
async def cmd_reload(interaction: discord.Interaction):
    try:
        data_manager.reload_all()
        await interaction.response.send_message("[OK] All game data reloaded.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"[ERROR] Failed to reload data: {str(e)}", ephemeral=True)

@bot.tree.command(name="charactercommands", description="List commands.")
async def cmd_help(interaction: discord.Interaction):
    text = """```text
>> AVAILABLE COMMANDS <<
/createcharacter   - Begin character creation
/sheet            - View your character sheet
/deletecharacter  - Delete all your characters (use --force to skip confirmation)
/reloaddata       - [Admin] Reload game data files
/charactercommands - Show this help message
```"""
    await interaction.response.send_message(text, ephemeral=True)

class CharacterListView(View):
    def __init__(self, user_chars, primary_id):
        super().__init__(timeout=120)
        for char_id, char in user_chars.items():
            label = f"{char.name} ({char.career})"
            if char_id == primary_id:
                label += " ★"
            self.add_item(Button(label=f"View: {label}", style=discord.ButtonStyle.primary, custom_id=f"view_{char_id}"))
            if char_id != primary_id:
                self.add_item(Button(label=f"Set Primary: {label}", style=discord.ButtonStyle.secondary, custom_id=f"primary_{char_id}"))
            self.add_item(Button(label=f"Delete: {label}", style=discord.ButtonStyle.danger, custom_id=f"delete_{char_id}"))
        self.add_item(Button(label="Exit", style=discord.ButtonStyle.secondary, custom_id="exit"))

class CharacterSheetView(View):
    def __init__(self, user_chars, primary_id, current_char_id, current_view="sheet"):
        super().__init__(timeout=120)
        self.add_item(Button(label="Back", style=discord.ButtonStyle.secondary, custom_id="back"))
        
        # Add buttons based on current view
        if current_view != "sheet":
            self.add_item(Button(label="Character Sheet", style=discord.ButtonStyle.secondary, custom_id=f"view_{current_char_id}"))
        if current_view != "inventory":
            self.add_item(Button(label="Inventory", style=discord.ButtonStyle.secondary, custom_id=f"inventory_{current_char_id}"))
        if current_view != "weapons":
            self.add_item(Button(label="Weapons", style=discord.ButtonStyle.secondary, custom_id=f"weapons_{current_char_id}"))
        if current_view != "loadout":
            self.add_item(Button(label="Loadout", style=discord.ButtonStyle.secondary, custom_id=f"loadout_{current_char_id}"))
        
        # Only show Set Primary button if this isn't already the primary character
        if current_char_id != primary_id:
            self.add_item(Button(label="Set as Primary", style=discord.ButtonStyle.primary, custom_id=f"primary_{current_char_id}"))
        self.add_item(Button(label="Delete Character", style=discord.ButtonStyle.danger, custom_id=f"delete_{current_char_id}"))

@bot.tree.command(name="characters", description="Manage your characters.")
async def cmd_characters(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    user_chars = data_manager.get_user_characters(user_id)
    primary_id = data_manager.primary_characters.get(user_id)
    if not user_chars:
        await interaction.response.send_message("```text\n[ERROR] No characters found.\n```", ephemeral=True)
        return
    char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
    for char_id, char in user_chars.items():
        is_primary = char_id == primary_id
        char_list.append(f"{char.name} ({char.career}){' ★' if is_primary else ''}")
    char_list.append("Use the buttons below to manage your characters.")
    char_list.append("```")
    await interaction.response.send_message('\n'.join(char_list), view=CharacterListView(user_chars, primary_id), ephemeral=True)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.type == discord.InteractionType.component:
        return
    custom_id = interaction.data.get("custom_id")
    user_id = str(interaction.user.id)
    user_chars = data_manager.get_user_characters(user_id)
    primary_id = data_manager.primary_characters.get(user_id)
    
    if custom_id == "exit":
        await interaction.response.edit_message(content="```text\n[INFO] Exited character management.\n```", view=None)
        return
    if custom_id == "back":
        char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
        for char_id, char in user_chars.items():
            is_primary = char_id == primary_id
            char_list.append(f"{char.name} ({char.career}){' ★' if is_primary else ''}")
        char_list.append("Use the buttons below to manage your characters.")
        char_list.append("```")
        await interaction.response.edit_message(content='\n'.join(char_list), view=CharacterListView(user_chars, primary_id))
        return
    if custom_id.startswith("view_"):
        char_id = custom_id[5:]
        char = user_chars.get(char_id)
        if not char:
            await interaction.response.edit_message(content="```text\n[ERROR] Character not found.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "sheet"))
            return
        sheet = ["```text", ">> CHARACTER SHEET <<"]
        # Basic Info
        sheet.append(f"\nName: {char.name}")
        sheet.append(f"Career: {char.career}")
        sheet.append("\n")
        # Personal Info
        sheet.append(f"Personal Agenda: {char.agenda}")
        sheet.append(f"Talent: {char.talent}")
        sheet.append(f"Signature Item: {char.signature_item}")
        sheet.append("\n")
        # Attributes
        sheet.append("Attributes:")
        for attr in ["Strength", "Agility", "Wits", "Empathy"]:
            value = getattr(char.attributes, attr.lower())
            sheet.append(f"  {attr}: {value} {format_attribute_bar(value)}")
        sheet.append("\n")
        # Skills
        sheet.append("Skills:")
        for skill_name, value in char.skills.__dict__.items():
            if value > 0:
                name = skill_name.replace('_', ' ').title()
                sheet.append(f"  {name}: {value} {format_skill_bar(value)}")
        sheet.append("```")
        await interaction.response.edit_message(content='\n'.join(sheet), view=CharacterSheetView(user_chars, primary_id, char_id, "sheet"))
    elif custom_id.startswith("inventory_"):
        char_id = custom_id[10:]
        char = user_chars.get(char_id)
        if not char:
            await interaction.response.edit_message(content="```text\n[ERROR] Character not found.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "inventory"))
            return
        if not char.inventory.items:
            await interaction.response.edit_message(content="```text\n[INVENTORY]\nYour inventory is empty.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "inventory"))
            return
        lines = ["```text", ">> INVENTORY <<"]
        for item in char.inventory.items:
            if isinstance(item, ConsumableItem):
                form = getattr(item, 'form', 'unit')
                form_plural = getattr(item, 'form_plural', 'units')
                lines.append(f"• {item.name} (x{item.quantity} {form if item.quantity == 1 else form_plural})")
            else:
                lines.append(f"• {item.name} (x{getattr(item, 'quantity', 1)})")
        lines.append("```")
        await interaction.response.edit_message(content='\n'.join(lines), view=CharacterSheetView(user_chars, primary_id, char_id, "inventory"))
    elif custom_id.startswith("weapons_"):
        char_id = custom_id[8:]
        char = user_chars.get(char_id)
        if not char:
            await interaction.response.edit_message(content="```text\n[ERROR] Character not found.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "weapons"))
            return
        if not char.weapons:
            await interaction.response.edit_message(content="```text\n[WEAPONS]\nNo weapons equipped.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "weapons"))
            return
        lines = ["```text", ">> WEAPONS <<\n"]
        # Primary weapon is the first in the list
        primary = char.weapons[0]
        skill, attr = get_skill_and_attr(primary)
        type_icon = get_type_icon(primary)
        ammo_icon = get_ammo_icon(primary)
        mods = get_modifiers(primary)
        lines.append("Primary Weapon")
        lines.append(f"{primary.name} | {type_icon} [{primary.damage_type}] | {ammo_icon} [ammo reloads] | 🎲 [{skill} + {attr} + *{mods}]")
        lines.append(f"💥 [damage] {primary.damage} | ✨ [bonus] +{primary.bonus} | 🎯[range]  {primary.range}")
        if primary.lore:
            lines.append(f'"{primary.lore}"')
        lines.append("")
        # Other weapons
        if len(char.weapons) > 1:
            lines.append("Other Weapons:")
            for i, weapon in enumerate(char.weapons[1:], 1):
                lines.append(f"{i}. {weapon.name}")
            lines.append("")
            lines.append("Options:")
            for i, weapon in enumerate(char.weapons[1:], 1):
                lines.append(f"[{i}] Switch to {weapon.name}")
            lines.append(f"[I] More info about primary weapon")
            for i, weapon in enumerate(char.weapons[1:], 1):
                lines.append(f"[I{i}] More info about {weapon.name}")
        lines.append("```")
        await interaction.response.edit_message(content='\n'.join(lines), view=CharacterSheetView(user_chars, primary_id, char_id, "weapons"))
    elif custom_id.startswith("loadout_"):
        char_id = custom_id[8:]
        char = user_chars.get(char_id)
        if not char:
            await interaction.response.edit_message(content="```text\n[ERROR] Character not found.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "loadout"))
            return
        if not char.loadout or not (char.loadout.suit or char.loadout.clothing or char.loadout.armor or char.loadout.accessories):
            await interaction.response.edit_message(content="```text\n[LOADOUT]\nNo wearables equipped.\n```", view=CharacterSheetView(user_chars, primary_id, char_id, "loadout"))
            return
        lines = ["```text"]
        lines.append(char.loadout.display_loadout())
        lines.append("```")
        await interaction.response.edit_message(content='\n'.join(lines), view=CharacterSheetView(user_chars, primary_id, char_id, "loadout"))
    elif custom_id.startswith("primary_"):
        char_id = custom_id[8:]
        if char_id == primary_id:
            await interaction.response.send_message("```text\n[INFO] This character is already your primary character.\n```", ephemeral=True)
            return
        data_manager.set_primary_character(user_id, char_id)
        # Update Discord roles and nickname
        user = await bot.fetch_user(int(user_id))
        for guild in bot.guilds:
            member = guild.get_member(user.id)
            if member:
                success, message = await update_user_roles_and_nickname(user, user_chars[char_id], guild)
                if not success:
                    logger.error(f"Failed to update roles in guild {guild.name}: {message}")
        # Update the view to reflect the new primary character
        if interaction.message.content.startswith("```text\n>> CHARACTER SHEET <<"):
            # If we're in the character sheet view, update that view
            await interaction.response.edit_message(content=f"```text\nSet {user_chars[char_id].name} as your primary character.\n```", view=CharacterSheetView(user_chars, char_id, char_id, "sheet"))
        else:
            # If we're in the character list view, update that view
            await interaction.response.edit_message(content=f"```text\nSet {user_chars[char_id].name} as your primary character.\n```", view=CharacterListView(user_chars, char_id))
    elif custom_id.startswith("delete_"):
        char_id = custom_id[7:]
        if char_id == primary_id and len(user_chars) > 1:
            await interaction.response.send_message("```text\n[ERROR] Cannot delete your primary character. Set another character as primary first.\n```", ephemeral=True)
            return
        del data_manager.characters[user_id][char_id]
        data_manager.save_characters()
        # Update the view to reflect the deletion
        if interaction.message.content.startswith("```text\n>> CHARACTER SHEET <<"):
            # If we're in the character sheet view, go back to the list view
            char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
            for cid, char in user_chars.items():
                if cid != char_id:  # Skip the deleted character
                    is_primary = cid == primary_id
                    char_list.append(f"{char.name} ({char.career}){' ★' if is_primary else ''}")
            char_list.append("Use the buttons below to manage your characters.")
            char_list.append("```")
            await interaction.response.edit_message(content='\n'.join(char_list), view=CharacterListView(user_chars, primary_id))
        else:
            # If we're in the character list view, update that view
            await interaction.response.edit_message(content=f"```text\nDeleted character {user_chars[char_id].name}.\n```", view=CharacterListView(user_chars, primary_id))

CAREER_EMOJIS = {
    "Colonial Marine": "🔫",
    "Colonial Marshal": "⭐",
    "Company Agent": "💼",
    "Medic": "💉",
    "Pilot": "✈️",
    "Roughneck": "🛠️",
    "Kid": "🧸",
    "Officer": "🎖️",
    "Wildcatter": "⛏️",
    "Scientist": "🧪",
    "Entertainer": "🎤"
}

async def update_user_roles_and_nickname(user: discord.User, character: Character, guild: discord.Guild) -> Tuple[bool, str]:
    """Update a user's roles and nickname based on their character."""
    try:
        member = guild.get_member(user.id)
        if not member:
            return False, f"User {user.name} not found in guild {guild.name}"

        # Get the career role with emoji
        emoji = CAREER_EMOJIS.get(character.career, "👤")
        role_name = f"{emoji} {character.career}"
        career_role = discord.utils.get(guild.roles, name=role_name)
        
        if not career_role:
            # Try to create the role if it doesn't exist
            try:
                career_role = await guild.create_role(
                    name=role_name,
                    reason=f"Career role for {character.name}",
                    hoist=True,
                    mentionable=False
                )
                log_debug(f"Created role: {role_name}")
            except discord.Forbidden:
                return False, f"Bot lacks permission to create role {role_name}"
            except discord.HTTPException as e:
                return False, f"Failed to create role {role_name}: {str(e)}"

        # Remove all career roles first
        success, message = await remove_character_roles(user, guild)
        if not success:
            return False, f"Failed to remove existing roles: {message}"

        # Add the new career role
        try:
            await member.add_roles(career_role)
            log_debug(f"Added role {career_role.name} to user {user.name}")
        except discord.Forbidden:
            return False, f"Bot lacks permission to add role {career_role.name}"
        except discord.HTTPException as e:
            return False, f"Failed to add role {career_role.name}: {str(e)}"

        # Update nickname if user is not the server owner
        if member.id != guild.owner_id:
            try:
                # Set nickname to just the emoji and character name
                new_nickname = f"{emoji} {character.name}"
                # If that's too long, truncate the character name
                if len(new_nickname) > 32:
                    max_name_length = 32 - len(emoji) - 2  # -2 for the space and emoji
                    new_nickname = f"{emoji} {character.name[:max_name_length]}"
                
                await member.edit(nick=new_nickname)
                log_debug(f"Updated nickname to {new_nickname} for user {user.name}")
            except discord.Forbidden:
                return False, f"Bot lacks permission to update nickname for {user.name}"
            except discord.HTTPException as e:
                return False, f"Failed to update nickname: {str(e)}"
            return True, f"Updated roles and nickname for {user.name}"
        else:
            return True, f"Updated roles for {user.name} (nickname unchanged for server owner)"

    except Exception as e:
        logger.error(f"Error updating roles and nickname: {e}")
        return False, f"Error updating roles and nickname: {str(e)}"

async def remove_character_roles(user: discord.User, guild: discord.Guild) -> Tuple[bool, str]:
    """Remove all career roles from a user."""
    try:
        member = guild.get_member(user.id)
        if not member:
            return False, f"User {user.name} not found in guild {guild.name}"

        # Get all career roles (those with emojis)
        career_roles = [role for role in guild.roles if any(emoji in role.name for emoji in CAREER_EMOJIS.values())]
        
        # Remove each career role
        for role in career_roles:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    log_debug(f"Removed role {role.name} from user {user.name}")
                except discord.Forbidden:
                    return False, f"Bot lacks permission to remove role {role.name}"
                except discord.HTTPException as e:
                    return False, f"Failed to remove role {role.name}: {str(e)}"

        return True, f"Removed all career roles from {user.name}"
    except Exception as e:
        logger.error(f"Error removing roles: {e}")
        return False, f"Error removing roles: {str(e)}"

async def set_primary_character(user_id: str, char_id: str, guild: Optional[discord.Guild] = None) -> bool:
    """Set a character as the user's primary character and update roles."""
    try:
        user = await bot.fetch_user(int(user_id))
        character = data_manager.characters[user_id][char_id]
        
        # Update primary character
        data_manager.primary_characters[user_id] = char_id
        data_manager.save_characters()
        
        # Update roles in all guilds where both bot and user are present
        if guild:
            success, message = await update_user_roles_and_nickname(user, character, guild)
            if not success:
                logger.error(f"Failed to update roles: {message}")
                return False
        else:
            for guild in bot.guilds:
                member = guild.get_member(user.id)
                if member:
                    success, message = await update_user_roles_and_nickname(user, character, guild)
                    if not success:
                        logger.error(f"Failed to update roles in guild {guild.name}: {message}")
        
        return True
    except Exception as e:
        logger.error(f"Error setting primary character: {e}")
        return False

async def delete_character(user_id: str, char_id: str, guild: Optional[discord.Guild] = None) -> bool:
    """Delete a character and handle primary character reassignment."""
    try:
        user = await bot.fetch_user(int(user_id))
        # Store if this was the primary character
        was_primary = char_id == data_manager.primary_characters.get(user_id)
        
        # Delete the character
        del data_manager.characters[user_id][char_id]
        
        # Handle primary character reassignment if needed
        if was_primary:
            remaining_chars = data_manager.get_user_characters(user_id)
            if remaining_chars:
                # Ask if they want to switch to another character
                char_list = ["```text", ">> SELECT NEW PRIMARY CHARACTER <<", ""]
                for cid, c in remaining_chars.items():
                    char_list.append(f"[{cid}] {c.name} ({c.career})")
                char_list.append("\nEnter the character ID to set as primary, or 'N' to create a new character.")
                char_list.append("```")
                
                await user.send('\n'.join(char_list))
                while True:
                    choice = await wait_for_user_message(user)
                    if choice.content.strip().upper() == "N":
                        # Start character creation
                        await user.send("```text\nStarting character creation process...\n```")
                        await cmd_create(discord.Interaction(bot, user))
                        return True
                    
                    # Check if the choice is a valid character ID
                    if choice.content.strip() in remaining_chars:
                        new_primary_id = choice.content.strip()
                        await set_primary_character(user_id, new_primary_id, guild)
                        await user.send(f"```text\n[OK] Set {remaining_chars[new_primary_id].name} as your primary character.\n```")
                        return True
                    else:
                        await user.send("```text\n[ERROR] Invalid choice. Please enter a valid character ID or 'N'.\n```")
            else:
                # No characters left - ask if they want to create a new one
                await user.send("""```text
You have no characters remaining. Would you like to:
[1] Create a new character
[2] Continue without a character (you can still observe)

Enter your choice (1 or 2):```""")
                
                while True:
                    choice = await wait_for_user_message(user)
                    if choice.content.strip() == "1":
                        # Start character creation
                        await user.send("```text\nStarting character creation process...\n```")
                        await cmd_create(discord.Interaction(bot, user))
                        return True
                    elif choice.content.strip() == "2":
                        # Remove all career roles
                        if guild:
                            success, message = await remove_character_roles(user, guild)
                            if not success:
                                logger.error(f"Failed to remove roles: {message}")
                        # Remove from primary characters
                        if user_id in data_manager.primary_characters:
                            del data_manager.primary_characters[user_id]
                        await user.send("```text\n[OK] You will continue without a character. You can still observe the game.\n```")
                        return True
                    else:
                        await user.send("```text\n[ERROR] Please enter 1 or 2.\n```")
        
        data_manager.save_characters()
        return True
    except Exception as e:
        logger.error(f"Error deleting character: {e}")
        return False

@bot.tree.command(name="inventory", description="View your character's inventory (non-equipped items).")
async def cmd_inventory(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    char = data_manager.get_primary_character(user_id)
    if not char:
        await interaction.response.send_message("```text\n[ERROR] No character sheet found.\n```", ephemeral=True)
        return
    if not char.inventory.items:
        await interaction.response.send_message("```text\n[INVENTORY]\nYour inventory is empty.\n```", ephemeral=True)
        return
    lines = ["```text", ">> INVENTORY <<"]
    for item in char.inventory.items:
        lines.append(f"• {item.name} (x{getattr(item, 'quantity', 1)})")
    lines.append("```")
    await interaction.response.send_message('\n'.join(lines), ephemeral=True)

@bot.tree.command(name="loadout", description="View your equipped wearables (loadout).")
async def cmd_loadout(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    char = data_manager.get_primary_character(user_id)
    if not char:
        await interaction.response.send_message("```text\n[ERROR] No character sheet found.\n```", ephemeral=True)
        return
    if not char.loadout or not (char.loadout.suit or char.loadout.clothing or char.loadout.armor or char.loadout.accessories):
        await interaction.response.send_message("```text\n[LOADOUT]\nNo wearables equipped.\n```", ephemeral=True)
        return
    # Use the WearableLoadout display method
    lines = ["```text"]
    lines.append(char.loadout.display_loadout())
    lines.append("```")
    await interaction.response.send_message('\n'.join(lines), ephemeral=True)

@bot.tree.command(name="weapons", description="View your equipped weapons.")
async def cmd_weapons(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    char = data_manager.get_primary_character(user_id)
    if not char:
        await interaction.response.send_message("```text\n[ERROR] No character sheet found.\n```", ephemeral=True)
        return
    if not char.weapons:
        await interaction.response.send_message("```text\n[WEAPONS]\nNo weapons equipped.\n```", ephemeral=True)
        return

    # --- Display ---
    lines = ["```text", ">> WEAPONS <<\n"]
    # Primary weapon is the first in the list
    primary = char.weapons[0]
    skill, attr = get_skill_and_attr(primary)
    type_icon = get_type_icon(primary)
    ammo_icon = get_ammo_icon(primary)
    mods = get_modifiers(primary)
    lines.append("Primary Weapon")
    lines.append(f"{primary.name} | {type_icon} [{primary.damage_type}] | {ammo_icon} [ammo reloads] | 🎲 [{skill} + {attr} + *{mods}]")
    lines.append(f"💥 [damage] {primary.damage} | ✨ [bonus] +{primary.bonus} | 🎯[range]  {primary.range}")
    if primary.lore:
        lines.append(f'\"{primary.lore}\"')
    lines.append("")
    # Other weapons
    if len(char.weapons) > 1:
        lines.append("Other Weapons:")
        for i, weapon in enumerate(char.weapons[1:], 1):
            lines.append(f"{i}. {weapon.name}")
        lines.append("")
        lines.append("Options:")
        for i, weapon in enumerate(char.weapons[1:], 1):
            lines.append(f"[{i}] Switch to {weapon.name}")
        lines.append(f"[I] More info about primary weapon")
        for i, weapon in enumerate(char.weapons[1:], 1):
            lines.append(f"[I{i}] More info about {weapon.name}")
    lines.append("```")
    await interaction.response.send_message('\n'.join(lines), ephemeral=True)

# Start the bot
bot.run(os.getenv('DISCORD_TOKEN'))