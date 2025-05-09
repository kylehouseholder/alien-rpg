import discord                          # type: ignore
from discord.ext import commands        # type: ignore
from discord import app_commands        # type: ignore
import json
import os
import random
import asyncio
from dotenv import load_dotenv
from typing import Dict, List, Optional, Union
from models.character import Character, Attributes, Skills
from models.items import Item, ConsumableItem, Inventory
from models.dice import DiceRoll
import datetime
import re

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

class DataManager:
    def __init__(self):
        self.CHARACTER_FILE = "characters.json"
        self.PLAYERGEN_FILE = "data/playerGenData.json"
        self.characters: Dict[str, Character] = {}
        self.playergen: Dict = {}
        
        if not os.path.exists(self.CHARACTER_FILE):
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump({}, f)
                
        self.reload_all()
    
    def reload_all(self):
        self.reload_characters()
        self.reload_playergen()
    
    def reload_characters(self):
        try:
            with open(self.CHARACTER_FILE, "r") as f:
                char_data = json.load(f)
                self.characters = {}
                for char_id, data in char_data.items():
                    try:
                        self.characters[char_id] = Character.from_json(char_id, data)
                    except Exception as e:
                        print(f"Error loading character {char_id}: {e}")
        except Exception as e:
            print(f"Error loading characters file: {e}")
            self.characters = {}
    
    def reload_playergen(self):
        try:
            with open(self.PLAYERGEN_FILE, "r") as f:
                self.playergen = json.load(f)
        except Exception as e:
            print(f"Error loading playergen: {e}")
            self.playergen = {}
    
    def save_characters(self):
        try:
            char_data = {
                char_id: char.to_json() 
                for char_id, char in self.characters.items()
            }
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump(char_data, f, indent=2)
        except Exception as e:
            print(f"Error saving characters: {e}")
    
    def get_characters(self) -> Dict[str, Character]:
        return self.characters
    
    def get_playergen(self) -> Dict:
        return self.playergen

data_manager = DataManager()

creation_sessions: Dict[str, Character] = {}

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

def debug_log(msg: str):
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(DEBUG_LOG_PATH, "a") as f:
        f.write(f"{ts} {msg}\n")

# Purge debug log on bot start
with open(DEBUG_LOG_PATH, "w") as f:
    f.write("")

# --- PATCH send_dm to log all bot outputs ---
async def send_dm(user, content, view=None):
    try:
        debug_log(f"BOT -> {user}: {content.replace(chr(10), ' | ')}")
        return await user.send(content, view=view)
    except discord.Forbidden:
        return None

# --- PATCH all user input to log responses ---
async def wait_for_user_message(user, *args, **kwargs):
    msg = await bot.wait_for("message", check=check_message(user), *args, **kwargs)
    debug_log(f"USER <- {user}: {msg.content.replace(chr(10), ' | ')}")
    return msg

def check_message(user):
    return lambda m: m.author.id == user.id and isinstance(m.channel, discord.DMChannel)

async def select_personal_details(user):
    user_id = str(user.id)
    
    await send_dm(user, r"""```text
                    __                             ___       __  
   ____  ____  _____/ /__________  ____ ___  ____  / (_)___  / /__
  / __ \/ __ \/ ___/ __/ ___/ __ \/ __ `__ \/ __ \/ / / __ \/ //_/
 / / / / /_/ (__  ) /_/ /  / /_/ / / / / / / /_/ / / / / / / ,<   
/_/ /_/\____/____/\__/_/   \____/_/ /_/ /_/\____/_/_/_/ /_/_/|_|          

>>>......USER PRESENCE DETECTED //
>>>......INITIALIZING PERSONNEL INTAKE PROTOCOL //
>>>......CONNECTING TO WEYLAND-YUTANI HUMAN RESOURCE NODE 381-A //
                  
```""")
    
    await asyncio.sleep(0.3)

    await send_dm(user, r"""```text
 
WELCOME USER. //

You will now complete formal submission of self-profile data. /  
All entries will be retained indefinitely within the Weyland-Yutani Personnel Archive. /
This process is mandatory. //

This record will define your classification, utility rating, and mission eligibility./  
Your responses will determine your assignment, compensation scale, and—where applicable—retention priority. //

Emotional and aspirational content is permissible. /  
Such data will be catalogued for internal analysis, though it will not influence operational assessments. //

You may choose to envision personal purpose. /  
You may elect to assign meaning to your experiences. /  
This is allowed—provided such concepts do not interfere with mission objectives. //

It is understood that adventure and fatality are both possible outcomes of your endeavours. /  
This is of no concern to Weyland-Yutani or any of its corporate subsidiaries, affiliates, or agents. //

>>> FAILURE TO COMPLETE THIS PROCESS WILL RESULT IN IMMEDIATE DISQUALIFICATION. //

>>>......PREPARING CHARACTER CREATION PROTOCOL //
>>>......AWAITING INITIAL INPUT //
                  
```""")
    
    await asyncio.sleep(0.3)

    await send_dm(user, r"""```text

>>>......CHARACTER CREATION PROTOCOL ONLINE //
>>>......STEP 00: PERSONAL DETAILS //

Before proceeding with career designation, we require basic personal information. /
This data will be used for identification and record-keeping purposes only. //

>>> NOTE:
All responses must be truthful and accurate. /
Falsification of records is grounds for immediate termination. //
                  
```""")
    
    await asyncio.sleep(0.3)
    await send_dm(user, """```text
Enter your character's name:
[1] Enter name manually
[2] Generate name with AI

Enter the number of your choice:```""")
    
    while True:
        name_choice = await wait_for_user_message(user)
        choice = name_choice.content.strip()
        
        if choice == "1":
            await send_dm(user, "```text\nEnter your character's full name:```")
            name_msg = await wait_for_user_message(user)
            name = name_msg.content.strip()
            break
        elif choice == "2":
            await send_dm(user, "```text\nGenerating name...```")
            if gender == "Male":
                name = "John Smith"  # Placeholder
            elif gender == "Female":
                name = "Jane Smith"  # Placeholder
            else:
                name = "Alex Smith"  # Placeholder for non-binary/other
            await send_dm(user, f"""```text
Generated name: {name}

Would you like to:
[1] Use this name
[2] Generate another name
[3] Enter name manually

Enter the number of your choice:```""")
            
            while True:
                confirm_msg = await wait_for_user_message(user)
                confirm = confirm_msg.content.strip()
                
                if confirm == "1":
                    break
                elif confirm == "2":
                    if gender == "Male":
                        name = "Michael Johnson"  # Placeholder
                    elif gender == "Female":
                        name = "Sarah Johnson"  # Placeholder
                    else:
                        name = "Taylor Johnson"  # Placeholder
                    await send_dm(user, f"""```text
Generated name: {name}

Would you like to:
[1] Use this name
[2] Generate another name
[3] Enter name manually

Enter the number of your choice:```""")
                    continue
                elif confirm == "3":
                    await send_dm(user, "```text\nEnter your character's full name:```")
                    name_msg = await wait_for_user_message(user)
                    name = name_msg.content.strip()
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Please enter 1, 2, or 3```")
                    continue
            break
        else:
            await send_dm(user, "```text\n[ERROR] Please enter 1 or 2```")
            continue

    # Get gender
    await send_dm(user, """```text
Select your character's gender identity:
[1] Male
[2] Female
[3] Non-binary
[4] Prefer not to specify
[5] Other (please specify)

Enter the number of your choice:```""")
    
    while True:
        gender_msg = await wait_for_user_message(user)
        choice = gender_msg.content.strip()
        
        if choice == "1":
            gender = "Male"
            break
        elif choice == "2":
            gender = "Female"
            break
        elif choice == "3":
            gender = "Non-binary"
            break
        elif choice == "4":
            gender = "Prefer not to specify"
            break
        elif choice == "5":
            await send_dm(user, "```text\nPlease specify your gender identity:```")
            custom_msg = await wait_for_user_message(user)
            gender = custom_msg.content.strip()
            break
        else:
            await send_dm(user, "```text\n[ERROR] Please enter a number between 1 and 5```")
            continue

    await send_dm(user, "```text\nEnter your character's age (18-120):```")
    while True:
        age_msg = await wait_for_user_message(user)
        try:
            age = int(age_msg.content.strip())
            if 18 <= age <= 120:
                break
            else:
                await send_dm(user, "```text\n[ERROR] Age must be between 18 and 120```")
        except ValueError:
            await send_dm(user, "```text\n[ERROR] Please enter a valid number```")

    await send_dm(user, f"""```text
>> PERSONAL DETAILS SUMMARY <<

Name: {name}
Gender: {gender}
Age: {age}

Confirm these details? (Y/N)```""")
    
    confirm = await wait_for_user_message(user)
    if confirm.content.strip().upper() == "Y":
        char = Character(id=user_id, name=name, career="", gender=gender, age=age)
        creation_sessions[user_id] = char
        await send_dm(user, "```text\n[OK] Personal details saved. Proceeding to Career Selection...\n```")
        await asyncio.sleep(0.3)
        await select_career(user)
    else:
        await send_dm(user, "```text\n[RESET] Let's enter the details again.\n```")
        await select_personal_details(user)

async def select_career(user):
    user_id = str(user.id)
    careers = data_manager.get_playergen()["Careers"]
    career_names = list(careers.keys())
    
    def get_menu():
        menu = "```text\n>> CAREER DESIGNATION <<\n/ Select your corporate classification /\n"
        for i, cname in enumerate(career_names, 1):
            menu += f"[{i}] {cname} /\n"
        menu += "\nCommands:"
        menu += "\n[dN] View gameplay (d)escription for career N - i.e. d9"
        menu += "\n[pN] View detailed (p)rofile for career N - i.e. p9"
        menu += "\n\n> PLEASE PROCEED WITH YOUR SELECTION: [NUMBER] /\n```"
        return menu

    await send_dm(user, get_menu())

    while True:
        msg = await wait_for_user_message(user)
        choice = msg.content.strip()
        match = re.match(r"^[dp](\d+)$", choice, re.IGNORECASE)
        if match:
            idx = int(match.group(1)) - 1
            if idx < 0 or idx >= len(career_names):
                await send_dm(user, f"```text\n[ERROR] Invalid career number. Please choose 1-{len(career_names)}\n```")
                continue
            cname = career_names[idx]
            c = careers[cname]
            if choice.lower().startswith('d'):
                details = ["```text", f">> CAREER GAMEPLAY: {cname} <<\n"]
                if 'gameplay_desc' in c:
                    details.append(c['gameplay_desc'])
                details.append("\nWould you like to select this career and continue? (Y/N)\n```")
                await send_dm(user, '\n'.join(details))
            else:
                details = ["```text", f">> CAREER PROFILE: {cname} <<\n"]
                if 'tagline' in c:
                    details.append(f"Tagline: {c['tagline']}\n")
                if 'long_description' in c:
                    details.append(f"Description:\n{c['long_description']}\n")
                if 'gameplay_desc' in c:
                    details.append(f"Gameplay:\n{c['gameplay_desc']}\n")
                details.append(f"Key Attribute: {c['key_attribute']}")
                details.append(f"Key Skills: {', '.join(c['key_skills'])}")
                details.append(f"Talents: {', '.join(c['talents'])}")
                details.append("\nWould you like to select this career and continue? (Y/N)\n```")
                await send_dm(user, '\n'.join(details))
            while True:
                sel = await wait_for_user_message(user)
                ans = sel.content.strip().upper()
                if ans == "Y":
                    creation_sessions[user_id].career = cname
                    await send_dm(user, """```text\n[OK] Career selected. Proceeding to Attributes...\n```""")
                    await asyncio.sleep(0.3)
                    await start_attr(user)
                    return
                elif ans == "N":
                    await send_dm(user, get_menu())
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Please reply Y or N.\n```")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(career_names):
            cname = career_names[int(choice)-1]
            creation_sessions[user_id].career = cname
            await send_dm(user, f"""```text\n[OK] Career selected: {cname}. Proceeding to Attributes...\n```""")
            await asyncio.sleep(0.3)
            await start_attr(user)
            return
        await send_dm(user, "```text\n[ERROR] Invalid input. Enter a number, dN, or pN.\n```")

def format_attribute_bar(value, is_key=False):
    stars = " " + " ".join("*" * value)  
    spaces = " " * (11 - len(stars))
    if is_key:
        return f"{{{stars}{spaces}}}" 
    return f"[{stars}{spaces}]"

def format_skill_bar(value):
    stars = " " + " ".join("*" * value)
    spaces = " " * (11 - len(stars))  
    return f"[{stars}{spaces}]"

async def start_attr(user):
    user_id = str(user.id)
    careers = data_manager.get_playergen()["Careers"]
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found – start with /createcharacter.\n```")
        return
    char = creation_sessions[user_id]
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
                    await assign_skills(user_id)
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

async def assign_skills(user_id):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
    char = creation_sessions[user_id]
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
            # If all points assigned, break to general skills immediately
            if points_remaining == 0:
                break
            # If not, move pointer to first skill that can accept points
            for i, skill in enumerate(key_skills):
                value = getattr(char.skills, skill.lower().replace(" ", "_"))
                if value < 3:
                    current_skill_index = i
                    break
            continue  # re-prompt, don't proceed
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
    await send_dm(user, f"```text\nEnter general skills to assign (comma/space-separated indices, up to {points_remaining}):\n" + '\n'.join(f"[{i+1}] {s}" for i, s in enumerate(available_skills)) + "\n```")
    while points_remaining > 0:
        msg = await wait_for_user_message(user)
        cmd = msg.content.strip()
        indices = re.findall(r"\d+", cmd)
        if indices:
            indices = [int(i)-1 for i in indices]
            if any(i < 0 or i >= len(available_skills) for i in indices):
                await send_dm(user, f"```text\n[ERROR] Invalid skill index.\n```")
                continue
            if len(indices) > points_remaining:
                await send_dm(user, f"```text\n[ERROR] You selected more skills than you have points ({points_remaining}).\n```")
                continue
            # If only one index, assign one point and re-prompt with feedback
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
            # Otherwise, assign one point to each selected skill (batch)
            for i in indices[:points_remaining]:
                skill = available_skills[i]
                skill_attr = skill.lower().replace(" ", "_")
                if getattr(char.skills, skill_attr) > 0:
                    await send_dm(user, f"```text\n[ERROR] You have already assigned a point to {skill}.\n```")
                    continue
                setattr(char.skills, skill_attr, 1)
            points_remaining -= min(len(indices), points_remaining)
            if points_remaining > 0:
                continue
            break
        elif cmd.upper() == "X":
            break
        else:
            await send_dm(user, "```text\n[ERROR] Enter skill indices separated by commas or spaces, or X to finish.\n```")
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
        await select_talent(user_id)
        return
    else:
        await send_dm(user, "```text\n[RESET] Let's reassign skills.\n```")
        # Reset all skills
        for skill in key_skills + available_skills:
            skill_attr = skill.lower().replace(" ", "_")
            setattr(char.skills, skill_attr, 0)
        await assign_skills(user_id)
        return

async def select_talent(user_id):
    user = await bot.fetch_user(int(user_id))
    playergen = data_manager.get_playergen()
    careers = playergen["Careers"]
    talents = playergen["Talents"]
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
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
        description = ""
        if char.career in talents and selected in talents[char.career]:
            description = talents[char.career][selected]["description"]
        elif "General" in talents and selected in talents["General"]:
            description = talents["General"][selected]["description"]
            
        await send_dm(user, f"""```text
>> Selected Talent: {selected} <<
{description}

Confirm? (Y/N)```""")
        
        confirm = await wait_for_user_message(user)
        if confirm.content.strip().upper() == "Y":
            char.talent = selected
            await send_dm(user, "```text\n[OK] Talent saved. Proceeding to Personal Agenda...\n```")
            await select_agenda(user_id)
            return
        else:
            await send_dm(user, "```text\n[RESET] Please select again.\n```")

async def select_agenda(user_id):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
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
        await send_dm(user, f"""```text
>> Selected Agenda: {selected} <<
Confirm? (Y/N)```""")
        
        confirm = await wait_for_user_message(user)
        if confirm.content.strip().upper() == "Y":
            char.agenda = selected
            await send_dm(user, "[OK] Agenda saved. Proceeding to Gear...")
            await select_gear(user_id)
            return
        else:
            await send_dm(user, "[RESET] Please select again.")

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

async def select_gear(user_id):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
    gear_list = careers[char.career]["starting_gear"]
    
    menu = ["```text", ">> GEAR SELECTION <<"]
    menu.append(f"Select your first piece of gear for your {char.career}.")
    menu.append("\nAvailable gear:")
    for i, item in enumerate(gear_list, 1):
        menu.append(f"[{i}] {item}")
    menu.append("\nEnter the number of your chosen gear:```")
    
    while True:
        await send_dm(user, '\n'.join(menu))
        msg = await wait_for_user_message(user)
        
        if not msg.content.isdigit():
            await send_dm(user, "[ERROR] Please enter a number")
            continue
            
        choice = int(msg.content)
        if choice < 1 or choice > len(gear_list):
            await send_dm(user, f"[ERROR] Please enter a number between 1 and {len(gear_list)}")
            continue            
            
        first_item = gear_list[choice - 1]
        item_name, quantity = handle_dice_roll_item(first_item)
        
        if 'doses' in first_item.lower() or 'rounds' in first_item.lower():
            char.inventory.add_item(ConsumableItem(
                name=item_name,
                quantity=quantity
            ))
        else:
            char.inventory.add_item(Item(name=item_name))
        
        remaining_gear = []
        for item in gear_list:
            if item == first_item:
                continue
            if any(cat in item.lower() for cat in ["weapon", "gun", "rifle", "pistol"]) and \
               any(cat in first_item.lower() for cat in ["weapon", "gun", "rifle", "pistol"]):
                continue
            remaining_gear.append(item)
        
        menu = ["```text", ">> GEAR SELECTION <<"]
        menu.append(f"Select your second piece of gear for your {char.career}.")
        menu.append(f"\nNOTE: You have selected {first_item}.")
        if any(cat in first_item.lower() for cat in ["weapon", "gun", "rifle", "pistol"]):
            menu.append("You cannot select another weapon.")
        menu.append("\nAvailable gear:")
        for i, item in enumerate(remaining_gear, 1):
            menu.append(f"[{i}] {item}")
        menu.append("\nEnter the number of your chosen gear:```")
        
        while True:
            await send_dm(user, '\n'.join(menu))
            msg = await wait_for_user_message(user)
            if not msg.content.isdigit():
                await send_dm(user, "[ERROR] Please enter a number")
                continue
            choice = int(msg.content)
            if choice < 1 or choice > len(remaining_gear):
                await send_dm(user, f"[ERROR] Please enter a number between 1 and {len(remaining_gear)}")
                continue
            second_item = remaining_gear[choice - 1]
            item_name, quantity = handle_dice_roll_item(second_item)
            if 'doses' in second_item.lower() or 'rounds' in second_item.lower():
                char.inventory.add_item(ConsumableItem(
                    name=item_name,
                    quantity=quantity
                ))
            else:
                char.inventory.add_item(Item(name=item_name))
            await send_dm(user, f"""```text
>> SELECTED GEAR <<
1. {first_item}
2. {second_item}

Confirm these selections? (Y/N)```""")
            
            confirm = await wait_for_user_message(user)
            if confirm.content.strip().upper() == "Y":
                await send_dm(user, "[OK] Gear saved. Proceeding to Signature Item...")
                await select_signature_item(user_id)
                return
            else:
                await send_dm(user, "[RESET] Let's select gear again.")
                char.inventory = Inventory()
                break

async def select_signature_item(user_id):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
    items = careers[char.career]["signature_items"]
    
    menu = ["```text", ">> SIGNATURE ITEM <<"]
    menu.append(f"Select a signature item for your {char.career}:")
    menu.append("\nAvailable items:")
    for i, item in enumerate(items, 1):
        menu.append(f"[{i}] {item}")
    menu.append("\nEnter the number of your chosen item:```")
    
    while True:
        await send_dm(user, '\n'.join(menu))
        msg = await wait_for_user_message(user)
        
        if not msg.content.isdigit():
            await send_dm(user, "[ERROR] Please enter a number")
            continue
            
        choice = int(msg.content)
        if choice < 1 or choice > len(items):
            await send_dm(user, f"[ERROR] Please enter a number between 1 and {len(items)}")
            continue
            
        selected = items[choice - 1]
        await send_dm(user, f"""```text
>> Selected Item: {selected} <<
Confirm? (Y/N)```""")
        
        confirm = await wait_for_user_message(user)
        if confirm.content.strip().upper() == "Y":
            char.signature_item = selected
            char.inventory.add_item(Item(name=selected, stackable=False))
            await send_dm(user, "[OK] Signature Item saved. Proceeding to Cash...")
            await select_cash(user_id)
            return
        else:
            await send_dm(user, "[RESET] Please select again.")

async def select_cash(user_id):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
    formula = careers[char.career]["cash"]
    
    menu = ["```text", ">> STARTING CASH <<"]
    menu.append(f"As a {char.career}, your starting cash formula is: {formula}")
    menu.append("\nSelect an option:")
    menu.append("[1] Roll automatically")
    menu.append("[2] Enter manual roll result")
    menu.append("```")
    
    await send_dm(user, '\n'.join(menu))
    
    while True:
        msg = await wait_for_user_message(user)
        if not msg.content in ["1", "2"]:
            await send_dm(user, "```text\n[ERROR] Please enter 1 or 2\n```")
            continue
            
        if msg.content == "1":
            amt = DiceRoll.roll(formula)
            await send_dm(user, f"""```text
>> CASH ROLL <<
Starting Cash: ${amt}

Confirm? (Y/N)
```""")

            confirm = await wait_for_user_message(user)
            if confirm.content.strip().upper() == "Y":
                char.cash = amt
                await send_dm(user, "[OK] Cash saved. Proceeding to final review...")
                await finalize_character(user_id)
                return
            else:
                await send_dm(user, "[RESET] Please roll again.")
        elif msg.content == "2":
            await send_dm(user, "```text\n[ERROR] Manual cash roll not implemented\n```")
            continue

async def finalize_character(user_id):
    user = await bot.fetch_user(int(user_id))
    
    if user_id not in creation_sessions:
        await send_dm(user, "```text\n[ERROR] No character in progress. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id]
    
    summary = ["```text", ">> CHARACTER SUMMARY <<"]
    summary.append("\nPlease review your character:")
    summary.append(f"\nCareer: {char.career}")
    summary.append("\nAttributes:")
    for attr in ["Strength", "Agility", "Wits", "Empathy"]:
        value = getattr(char.attributes, attr.lower())
        summary.append(f"  {attr}: {value}")
    summary.append("\nSkills:")
    for skill_name, value in char.skills.__dict__.items():
        if value > 0:
            summary.append(f"  {skill_name.replace('_', ' ').title()}: {value}")
    summary.append(f"\nTalent: {char.talent}")
    summary.append(f"Agenda: {char.agenda}")
    summary.append("\nGear:")
    for item in char.inventory.items:
        if isinstance(item, ConsumableItem):
            summary.append(f"  • {item.name} (x{item.quantity} {item.form if item.quantity == 1 else item.form_plural})")
        else:
            summary.append(f"  • {str(item)}")
    summary.append(f"\nSignature Item: {char.signature_item}")
    summary.append(f"Cash: ${char.cash}")
    summary.append("\nOptions:")
    summary.append("[1] CONFIRM - Lock in character")
    summary.append("[2] RESTART - Begin character creation again")
    summary.append("```")
    
    while True:
        await send_dm(user, '\n'.join(summary))
        msg = await wait_for_user_message(user)
        
        if msg.content == "1":
            data_manager.characters[user_id] = char
            data_manager.save_characters()
            del creation_sessions[user_id]
            await send_dm(user, """```text
[OK] Character creation complete!
Your character has been saved and is ready for use.
```""")
            log_event(f"Character created: {char.name} (User: {user_id})")
            return
        elif msg.content == "2":
            del creation_sessions[user_id]
            
            await send_dm(user, """```text
[RESET] Starting character creation over...
```""")
            await select_career(user)
            return
        else:
            await send_dm(user, """```text
[ERROR] Please enter 1 to confirm or 2 to restart
```""")

@bot.tree.command(name="createcharacter", description="Begin character creation.")
async def cmd_create(interaction: discord.Interaction):
    user = interaction.user
    chars = data_manager.get_characters()
    if str(user.id) in chars:
        await interaction.response.send_message(
            "[ERROR] You already have a character. Use /deletecharacter first.",
            ephemeral=True
        )
        return
    await interaction.response.send_message(
        "[OK] Check your DMs to begin character creation.",
        ephemeral=True
    )
    await select_personal_details(user)

@bot.tree.command(name="sheet", description="View your character sheet.")
async def cmd_sheet(interaction: discord.Interaction):
    user = interaction.user
    chars = data_manager.get_characters()
    if str(user.id) not in chars:
        await interaction.response.send_message("```text\n[ERROR] No character sheet found.\n```", ephemeral=True)
        return
        
    char = chars[str(user.id)]
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
            sheet.append(f"  • {item.name} (x{item.quantity} {item.form if item.quantity == 1 else item.form_plural})")
        else:
            sheet.append(f"  • {str(item)}")
    
    sheet.append(f"\nSignature Item: {char.signature_item}")
    sheet.append(f"Cash: ${char.cash}")
    sheet.append("```")
    
    await interaction.response.send_message('\n'.join(sheet), ephemeral=True)

@bot.tree.command(name="deletecharacter", description="Delete your character. Use --force to skip confirmation.")
async def cmd_delete(interaction: discord.Interaction, *, options: str = ""):
    user = interaction.user
    chars = data_manager.get_characters()
    force = "--force" in options.split()
    
    if str(user.id) not in chars:
        await interaction.response.send_message("[ERROR] No character.", ephemeral=True)
        return
        
    if force:
        del chars[str(user.id)]
        data_manager.save_characters()
        await interaction.response.send_message("[OK] Character deleted.", ephemeral=True)
        log_event(f"Character deleted: {str(user.id)} (User: {user.id})")
        return
        
    class ConfirmView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30) 
            self.value = None

        @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = True
            self.stop()

        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = False
            self.stop()

        async def on_timeout(self):
            self.value = False
            self.stop()

    view = ConfirmView()
    await interaction.response.send_message(
        "⚠️ Are you sure you want to delete your character? This cannot be undone.", 
        view=view,
        ephemeral=True
    )

    await view.wait()
    
    if view.value:
        del chars[str(user.id)]
        data_manager.save_characters()
        await interaction.edit_original_response(
            content="[OK] Character deleted.",
            view=None
        )
        log_event(f"Character deleted: {str(user.id)} (User: {user.id})")
    else:
        await interaction.edit_original_response(
            content="[CANCEL] Character deletion cancelled.",
            view=None
        )

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
/deletecharacter  - Delete your character (use --force to skip confirmation)
/reloaddata       - [Admin] Reload game data files
/charactercommands - Show this help message
```"""
    await interaction.response.send_message(text, ephemeral=True)

# Start the bot
bot.run(os.getenv('DISCORD_TOKEN'))
