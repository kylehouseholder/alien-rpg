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
import copy  # Add at the top with other imports
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        self.characters: Dict[str, Dict[str, Character]] = {}  # user_id -> {char_id -> Character}
        self.primary_characters: Dict[str, str] = {}  # user_id -> primary_char_id
        self.playergen: Dict = {}
        
        if not os.path.exists(self.CHARACTER_FILE):
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump({"characters": {}, "primary_characters": {}}, f)
                
        self.reload_all()
    
    def reload_all(self):
        self.reload_characters()
        self.reload_playergen()
    
    def reload_characters(self):
        try:
            with open(self.CHARACTER_FILE, "r") as f:
                data = json.load(f)
                self.primary_characters = data.get("primary_characters", {})
                
                # Convert dictionary data to Character objects
                self.characters = {}
                for user_id, user_chars in data.get("characters", {}).items():
                    self.characters[user_id] = {}
                    for char_id, char_data in user_chars.items():
                        # Convert attributes
                        attrs = Attributes(
                            strength=char_data["Attributes"]["Strength"],
                            agility=char_data["Attributes"]["Agility"],
                            wits=char_data["Attributes"]["Wits"],
                            empathy=char_data["Attributes"]["Empathy"]
                        )
                        
                        # Convert skills
                        skills = Skills()
                        for skill_name, value in char_data["Skills"].items():
                            setattr(skills, skill_name.lower(), value)
                        
                        # Convert inventory
                        inventory = Inventory()
                        for gear_item in char_data["Gear"]:
                            if "x" in gear_item:
                                name, quantity = gear_item.split(" (x")
                                quantity = int(quantity.rstrip(")"))
                                if any(word in name.lower() for word in ["pills", "rounds", "doses"]):
                                    inventory.add_item(ConsumableItem(name=name, quantity=quantity))
                                else:
                                    inventory.add_item(Item(name=name, quantity=quantity))
                            else:
                                inventory.add_item(Item(name=gear_item))
                        
                        # Create Character object
                        char = Character(
                            id=char_id,
                            name=char_data["Name"],
                            career=char_data["Career"],
                            gender=char_data["Gender"],
                            age=char_data["Age"],
                            attributes=attrs,
                            skills=skills,
                            talent=char_data["Talent"],
                            agenda=char_data["Agenda"],
                            inventory=inventory,
                            signature_item=char_data["Signature Item"],
                            cash=char_data["Cash"]
                        )
                        self.characters[user_id][char_id] = char
                
        except Exception as e:
            print(f"Error loading characters file: {e}")
            self.characters = {}
            self.primary_characters = {}
    
    def reload_playergen(self):
        try:
            with open(self.PLAYERGEN_FILE, "r") as f:
                self.playergen = json.load(f)
        except Exception as e:
            print(f"Error loading playergen: {e}")
            self.playergen = {}
    
    def get_playergen(self) -> Dict:
        """Get the playergen data"""
        return self.playergen
    
    def save_characters(self):
        try:
            data = {
                "characters": {
                    user_id: {
                        char_id: copy.deepcopy(char.to_json())
                        for char_id, char in user_chars.items()
                    }
                    for user_id, user_chars in self.characters.items()
                },
                "primary_characters": self.primary_characters
            }
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving characters: {e}")
    
    def get_characters(self) -> Dict[str, Dict[str, Character]]:
        return self.characters
    
    def get_user_characters(self, user_id: str) -> Dict[str, Character]:
        return self.characters.get(user_id, {})

    def get_primary_character(self, user_id: str) -> Optional[Character]:
        """Get a user's primary character"""
        if user_id not in self.primary_characters:
            return None
        char_id = self.primary_characters[user_id]
        return self.characters.get(user_id, {}).get(char_id)
    
    def set_primary_character(self, user_id: str, char_id: str) -> bool:
        """Set a user's primary character. Returns True if successful."""
        try:
            # Check if the user has any characters
            if user_id not in self.characters:
                logger.error(f"User {user_id} has no characters")
                return False
            
            # Check if the character exists for this user
            if char_id not in self.characters[user_id]:
                logger.error(f"Character {char_id} not found for user {user_id}")
                return False
            
            # Set the primary character
            self.primary_characters[user_id] = char_id
            self.save_characters()
            logger.debug(f"Set primary character for user {user_id} to {char_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting primary character: {e}")
            return False

data_manager = DataManager()

creation_sessions: Dict[str, Dict[str, Character]] = {}

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

async def select_personal_details(user, char_id: str):
    user_id = str(user.id)
    logger.debug(f"Starting personal details for user {user_id}, char {char_id}")
    
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
Enter your character's full name:
(Only letters, spaces, and hyphens allowed.)
```""")
    while True:
        name_msg = await wait_for_user_message(user)
        name = name_msg.content.strip()
        # Accept only letters, spaces, and hyphens
        if re.match(r'^[A-Za-z\- ]+$', name) and len(name) > 1:
            break
        else:
            await send_dm(user, """```text
[ERROR] Please enter a valid name using only letters, spaces, and hyphens.
Try again:
```""")

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
        logger.debug(f"Creating new character for user {user_id}, char {char_id}")
        char = Character(id=char_id, name=name, career="", gender=gender, age=age)
        if user_id not in creation_sessions:
            creation_sessions[user_id] = {}
        creation_sessions[user_id][char_id] = char
        logger.debug(f"Character created and stored in session: {char.name}")
        await send_dm(user, "```text\n[OK] Personal details saved. Proceeding to Career Selection...\n```")
        await asyncio.sleep(0.3)
        await select_career(user, char_id)
    else:
        await send_dm(user, "```text\n[RESET] Let's enter the details again.\n```")
        await select_personal_details(user, char_id)

async def select_career(user, char_id: str):
    user_id = str(user.id)
    logger.debug(f"Starting career selection for user {user_id}, char {char_id}")
    
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        logger.error(f"No character found in session for user {user_id}, char {char_id}")
        await send_dm(user, "```text\n[ERROR] Character creation session lost. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id][char_id]
    logger.debug(f"Found character in session: {char.name}")
    
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
                    creation_sessions[user_id][char_id].career = cname
                    await send_dm(user, """```text\n[OK] Career selected. Proceeding to Attributes...\n```""")
                    await asyncio.sleep(0.3)
                    await start_attr(user, char_id)
                    return
                elif ans == "N":
                    await send_dm(user, get_menu())
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Please reply Y or N.\n```")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(career_names):
            cname = career_names[int(choice)-1]
            creation_sessions[user_id][char_id].career = cname
            await send_dm(user, f"""```text\n[OK] Career selected: {cname}. Proceeding to Attributes...\n```""")
            await asyncio.sleep(0.3)
            await start_attr(user, char_id)
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

async def select_gear(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id][char_id]
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
                await select_signature_item(user_id, char_id)
                return
            else:
                await send_dm(user, "[RESET] Let's select gear again.")
                char.inventory = Inventory()
                break

async def select_signature_item(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
        
    char = creation_sessions[user_id][char_id]
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
        char.signature_item = selected
        await send_dm(user, "[OK] Signature Item saved. Proceeding to Cash...")
        # Immediately apply cash and proceed to final review
        await apply_starting_cash_and_finalize(user_id, char_id)
        return

async def apply_starting_cash_and_finalize(user_id, char_id: str):
    user = await bot.fetch_user(int(user_id))
    careers = data_manager.get_playergen()["Careers"]
    char = creation_sessions[user_id][char_id]
    formula = careers[char.career]["cash"]
    amt = DiceRoll.roll(formula)
    char.cash = amt
    await send_dm(user, "[OK] Cash assigned. Proceeding to final review...")
    await finalize_character(user_id, char_id, finalstep=True)

async def finalize_character(user_id, char_id: str, finalstep=False):
    user = await bot.fetch_user(int(user_id))
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No character in progress. Please start over with /createcharacter.\n```")
        return
    char = creation_sessions[user_id][char_id]
    while True:
        summary = ["```text", ">> CHARACTER SUMMARY <<"]
        summary.append("\nPlease review...")
        summary.append(f"\n[A] Character: {char.name}, {char.gender}, {char.age}")
        summary.append(f"\n[B] Career: {char.career}")
        summary.append(f"\n[C] Talent: {char.talent}")
        summary.append(f"\n[D] Agenda: {char.agenda}")
        summary.append(" \n[E] Attributes:")
        for attr in ["Strength", "Agility", "Wits", "Empathy"]:
            value = getattr(char.attributes, attr.lower())
            summary.append(f"  {attr}: {value}")
        summary.append("\n[F] Skills:")
        for skill_name, value in char.skills.__dict__.items():
            if value > 0:
                summary.append(f"  {skill_name.replace('_', ' ').title()}: {value}")
        summary.append(f"\n[G] Gear:")
        for item in char.inventory.items:
            if isinstance(item, ConsumableItem):
                # Use default values if form/form_plural are not set
                form = getattr(item, 'form', 'unit')
                form_plural = getattr(item, 'form_plural', 'units')
                summary.append(f"  • {item.name} (x{item.quantity} {form if item.quantity == 1 else form_plural})")
            else:
                summary.append(f"  • {str(item)}")
        summary.append(f"  • Cash: ${char.cash}")
        summary.append(f"\n[H] Signature Item: {char.signature_item}")
        summary.append("\nOptions:")
        summary.append("[1] CONFIRM - Lock in character")
        summary.append("[0] RESTART - Purge this sheet, start over at the beginning.")
        summary.append("\nEnter any letter to return to that section and make changes.")
        summary.append("```")
        await send_dm(user, '\n'.join(summary))
        msg = await wait_for_user_message(user)
        choice = msg.content.strip().upper()
        if choice == "1":
            logger.debug(f"Saving character {char.name} for user {user_id}")
            if user_id not in data_manager.characters:
                data_manager.characters[user_id] = {}
            data_manager.characters[user_id][char_id] = char
            
            # Set as primary character if it's the user's first character
            if not data_manager.primary_characters.get(user_id):
                data_manager.primary_characters[user_id] = char_id
                logger.debug(f"Set {char.name} as primary character for user {user_id}")
            
            data_manager.save_characters()
            logger.debug(f"Characters after save: {data_manager.characters}")
            logger.debug(f"Primary characters after save: {data_manager.primary_characters}")
            
            del creation_sessions[user_id][char_id]
            await send_dm(user, """```text\n[OK] Character creation complete!\nYour character has been saved and is ready for use.\n```""")
            log_event(f"Character created: {char.name} (User: {user_id}, Char: {char_id})")
            return
        elif choice == "0":
            await send_dm(user, """```text\nAre you sure you want to restart character creation? This will erase all progress. (Y/N)\n```""")
            confirm = await wait_for_user_message(user)
            if confirm.content.strip().upper() == "Y":
                del creation_sessions[user_id][char_id]
                await send_dm(user, """```text\n[RESET] Starting character creation over...\n```""")
                await select_career(user, char_id)
                return
            else:
                continue
        elif finalstep and choice in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            # Call the appropriate edit function for the section, then return to summary
            await edit_section(user_id, char_id, choice)
            continue
        else:
            await send_dm(user, "```text\n[ERROR] Please enter a valid option.\n```")
            continue

# Placeholder for section editing logic
async def edit_section(user_id, char_id, section):
    user = await bot.fetch_user(int(user_id))
    # Implement section-specific editing logic here
    await send_dm(user, f"```text\n[EDIT] Section {section} editing not yet implemented. Returning to summary...\n```")
    return

@bot.tree.command(name="createcharacter", description="Begin character creation.")
async def cmd_create(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    user_chars = data_manager.get_user_characters(user_id)
    
    # Generate a unique character ID
    char_id = f"{user.id}_{len(user_chars) + 1}"
    logger.debug(f"Starting character creation for user {user_id}, char {char_id}")
    
    # Initialize the user's session if needed
    if user_id not in creation_sessions:
        creation_sessions[user_id] = {}
    
    # Clear any existing session for this character
    if char_id in creation_sessions[user_id]:
        del creation_sessions[user_id][char_id]
    
    await interaction.response.send_message(
        "[OK] Check your DMs to begin character creation.",
        ephemeral=True
    )
    await select_personal_details(user, char_id)

@bot.tree.command(name="sheet", description="View your character sheet.")
async def cmd_sheet(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    logger.debug(f"Sheet command called by user {user_id}")
    logger.debug(f"All characters: {data_manager.characters}")
    logger.debug(f"Primary characters: {data_manager.primary_characters}")
    
    char = data_manager.get_primary_character(user_id)
    logger.debug(f"Found primary character: {char}")
    
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

@bot.tree.command(name="deletecharacter", description="Delete your character. Use --force to skip confirmation.")
async def cmd_delete(interaction: discord.Interaction, *, options: str = ""):
    user = interaction.user
    user_id = str(user.id)
    chars = data_manager.get_user_characters(user_id)
    force = "--force" in options.split()
    
    if not chars:
        await interaction.response.send_message("[ERROR] No character.", ephemeral=True)
        return
        
    if force:
        # Create a list of character IDs to delete
        char_ids = list(chars.keys())
        for char_id in char_ids:
            del data_manager.characters[user_id][char_id]
        # Also remove from primary characters if needed
        if user_id in data_manager.primary_characters:
            del data_manager.primary_characters[user_id]
        data_manager.save_characters()
        await interaction.response.send_message("[OK] All characters deleted.", ephemeral=True)
        log_event(f"All characters deleted: {user_id} (User: {user.id})")
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
        "⚠️ Are you sure you want to delete all your characters? This cannot be undone.", 
        view=view,
        ephemeral=True
    )

    await view.wait()
    
    if view.value:
        # Create a list of character IDs to delete
        char_ids = list(chars.keys())
        for char_id in char_ids:
            del data_manager.characters[user_id][char_id]
        # Also remove from primary characters if needed
        if user_id in data_manager.primary_characters:
            del data_manager.primary_characters[user_id]
        data_manager.save_characters()
        await interaction.edit_original_response(
            content="[OK] All characters deleted.",
            view=None
        )
        log_event(f"All characters deleted: {user_id} (User: {user.id})")
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
/deletecharacter  - Delete all your characters (use --force to skip confirmation)
/reloaddata       - [Admin] Reload game data files
/charactercommands - Show this help message
```"""
    await interaction.response.send_message(text, ephemeral=True)

@bot.tree.command(name="characters", description="Manage your characters - view details, set primary, or delete characters.")
async def cmd_characters(interaction: discord.Interaction):
    user = interaction.user
    user_id = str(user.id)
    user_chars = data_manager.get_user_characters(user_id)
    
    if not user_chars:
        await interaction.response.send_message("```text\n[ERROR] No characters found.\n```", ephemeral=True)
        return
    
    primary_id = data_manager.primary_characters.get(user_id)
    
    # Create a view with buttons for each character
    class CharacterView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
            
            # Add a button for each character
            for char_id, char in user_chars.items():
                is_primary = char_id == primary_id
                label = f"★ {char.name}" if is_primary else char.name
                button = discord.ui.Button(
                    label=label,
                    custom_id=char_id,
                    style=discord.ButtonStyle.primary if is_primary else discord.ButtonStyle.secondary
                )
                button.callback = self.button_callback
                self.add_item(button)
        
        async def button_callback(self, interaction: discord.Interaction):
            try:
                char_id = interaction.data["custom_id"]
                char = user_chars[char_id]
                
                # Create a new view for character actions
                class CharacterActionView(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout=60)
                        
                        # Add Set Primary button if not already primary
                        if char_id != primary_id:
                            set_primary = discord.ui.Button(
                                label="Set as Primary",
                                style=discord.ButtonStyle.success,
                                custom_id="set_primary"
                            )
                            set_primary.callback = self.set_primary_callback
                            self.add_item(set_primary)
                        
                        # Add Delete button
                        delete = discord.ui.Button(
                            label="Delete Character",
                            style=discord.ButtonStyle.danger,
                            custom_id="delete"
                        )
                        delete.callback = self.delete_callback
                        self.add_item(delete)
                        
                        # Add View Sheet button
                        view_sheet = discord.ui.Button(
                            label="View Sheet",
                            style=discord.ButtonStyle.secondary,
                            custom_id="view_sheet"
                        )
                        view_sheet.callback = self.view_sheet_callback
                        self.add_item(view_sheet)
                        
                        # Add Back button
                        back = discord.ui.Button(
                            label="← Back to List",
                            style=discord.ButtonStyle.secondary,
                            custom_id="back"
                        )
                        back.callback = self.back_callback
                        self.add_item(back)
                        
                        # Add Close button
                        close = discord.ui.Button(
                            label="Close",
                            style=discord.ButtonStyle.secondary,
                            custom_id="close"
                        )
                        close.callback = self.close_callback
                        self.add_item(close)
                    
                    async def set_primary_callback(self, interaction: discord.Interaction):
                        if data_manager.set_primary_character(user_id, char_id):
                            await interaction.response.send_message(
                                f"```text\n[OK] {char.name} is now your primary character.\n```",
                                ephemeral=True
                            )
                        else:
                            await interaction.response.send_message(
                                "```text\n[ERROR] Failed to set primary character.\n```",
                                ephemeral=True
                            )
                    
                    async def delete_callback(self, interaction: discord.Interaction):
                        # Create confirmation view
                        class ConfirmDeleteView(discord.ui.View):
                            def __init__(self):
                                super().__init__(timeout=30)
                            
                            @discord.ui.button(label="Confirm Delete", style=discord.ButtonStyle.danger)
                            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                                try:
                                    del data_manager.characters[user_id][char_id]
                                    if primary_id == char_id:
                                        del data_manager.primary_characters[user_id]
                                    data_manager.save_characters()
                                    await interaction.response.send_message(
                                        f"```text\n[OK] {char.name} has been deleted.\n```",
                                        ephemeral=True
                                    )
                                except Exception as e:
                                    logger.error(f"Error deleting character: {e}")
                                    await interaction.response.send_message(
                                        "```text\n[ERROR] Failed to delete character.\n```",
                                        ephemeral=True
                                    )
                            
                            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
                            async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
                                await interaction.response.send_message(
                                    "```text\n[CANCEL] Character deletion cancelled.\n```",
                                    ephemeral=True
                                )
                        
                        await interaction.response.send_message(
                            f"```text\n⚠️ Are you sure you want to delete {char.name}? This cannot be undone.\n```",
                            view=ConfirmDeleteView(),
                            ephemeral=True
                        )
                    
                    async def view_sheet_callback(self, interaction: discord.Interaction):
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
                                form = getattr(item, 'form', 'unit')
                                form_plural = getattr(item, 'form_plural', 'units')
                                sheet.append(f"  • {item.name} (x{item.quantity} {form if item.quantity == 1 else form_plural})")
                            else:
                                sheet.append(f"  • {str(item)}")
                        sheet.append(f"\nSignature Item: {char.signature_item}")
                        sheet.append(f"Cash: ${char.cash}")
                        sheet.append("```")
                        
                        await interaction.response.send_message('\n'.join(sheet), ephemeral=True)
                    
                    async def back_callback(self, interaction: discord.Interaction):
                        # Recreate the character list view
                        char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
                        for char_id, char in user_chars.items():
                            is_primary = char_id == primary_id
                            char_list.append(f"{'★ ' if is_primary else ''}{char.name} ({char.career})")
                        char_list.append("\nClick a character to manage them.")
                        char_list.append("```")
                        
                        await interaction.response.edit_message(
                            content='\n'.join(char_list),
                            view=CharacterView()
                        )
                    
                    async def close_callback(self, interaction: discord.Interaction):
                        try:
                            await interaction.response.edit_message(
                                content="```text\n[CLOSED] Character management interface closed.\n```",
                                view=None
                            )
                        except Exception as e:
                            logger.error(f"Error closing character interface: {e}")
                            await interaction.response.send_message(
                                "```text\n[ERROR] Failed to close interface.\n```",
                                ephemeral=True
                            )
                
                # Create character summary
                summary = ["```text", f">> CHARACTER: {char.name} <<"]
                summary.append(f"Career: {char.career}")
                summary.append(f"Gender: {char.gender}")
                summary.append(f"Age: {char.age}")
                summary.append("\nKey Attributes:")
                for attr in ["Strength", "Agility", "Wits", "Empathy"]:
                    value = getattr(char.attributes, attr.lower())
                    summary.append(f"  {attr}: {value}")
                summary.append(f"\nTalent: {char.talent}")
                summary.append(f"Cash: ${char.cash}")
                summary.append("\nSelect an action:")
                summary.append("```")
                
                await interaction.response.send_message(
                    '\n'.join(summary),
                    view=CharacterActionView(),
                    ephemeral=True
                )
                
            except Exception as e:
                logger.error(f"Error in button callback: {e}")
                await interaction.response.send_message(
                    "```text\n[ERROR] An error occurred while managing character.\n```",
                    ephemeral=True
                )
    
    # Show the character list
    char_list = ["```text", ">> YOUR CHARACTERS <<", ""]
    for char_id, char in user_chars.items():
        is_primary = char_id == primary_id
        char_list.append(f"{'★ ' if is_primary else ''}{char.name} ({char.career})")
    char_list.append("\nClick a character to manage them.")
    char_list.append("```")
    
    await interaction.response.send_message(
        "\n".join(char_list),
        view=CharacterView(),
        ephemeral=True
    )

# Start the bot
bot.run(os.getenv('DISCORD_TOKEN'))
