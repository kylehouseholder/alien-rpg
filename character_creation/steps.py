# Character creation step functions moved from main.py

# Add necessary imports
import asyncio
import re
from typing import Dict
from models.character import Character, Attributes, Skills
from models.items import Item, ConsumableItem, Inventory
from models.dice import DiceRoll
from data_manager import data_manager
import logging
import datetime
from character_creation.utils import (
    format_attribute_bar, format_skill_bar, get_paired_gear, get_article_for_item, find_wearable_by_name, find_weapon_by_name, handle_dice_roll_item
)

# NOTE: The following must be provided by the caller (main.py):
# - send_dm
# - wait_for_user_message
# - creation_sessions
# - logger

# All functions below require send_dm, wait_for_user_message, and creation_sessions to be passed in as arguments or available in the calling context.

async def select_personal_details(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    user_id = str(user.id)
    logger.debug(f"Starting personal details for user {user_id}, char {char_id}")
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        logger.error(f"No valid session found for user {user_id}, char {char_id}")
        await send_dm(user, "```text\n[ERROR] Character creation session lost. Please start over with /createcharacter.\n```")
        return
    if user_id in creation_sessions and char_id in creation_sessions[user_id]:
        del creation_sessions[user_id][char_id]
    if user_id not in creation_sessions:
        creation_sessions[user_id] = {}
    creation_sessions[user_id][char_id] = Character(
        id=char_id,
        name="",
        career="",
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
    try:
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
            if re.match(r'^[A-Za-z\- ]+$', name) and len(name) > 1:
                creation_sessions[user_id][char_id].name = name
                break
            else:
                await send_dm(user, """```text
[ERROR] Please enter a valid name using only letters, spaces, and hyphens.
Try again:
```""")
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
                creation_sessions[user_id][char_id].gender = "Male"
                break
            elif choice == "2":
                creation_sessions[user_id][char_id].gender = "Female"
                break
            elif choice == "3":
                creation_sessions[user_id][char_id].gender = "Non-binary"
                break
            elif choice == "4":
                creation_sessions[user_id][char_id].gender = "Prefer not to specify"
                break
            elif choice == "5":
                await send_dm(user, "```text\nPlease specify your gender identity:```")
                custom_msg = await wait_for_user_message(user)
                creation_sessions[user_id][char_id].gender = custom_msg.content.strip()
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
                    creation_sessions[user_id][char_id].age = age
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Age must be between 18 and 120```")
            except ValueError:
                await send_dm(user, "```text\n[ERROR] Please enter a valid number```")
        char = creation_sessions[user_id][char_id]
        await send_dm(user, f"""```text
>> PERSONAL DETAILS SUMMARY <<

Name: {char.name}
Gender: {char.gender}
Age: {char.age}

Confirm these details? (Y/N)```""")
        confirm = await wait_for_user_message(user)
        if confirm.content.strip().upper() == "Y":
            logger.debug(f"Personal details confirmed for user {user_id}, char {char_id}")
            await send_dm(user, "```text\n[OK] Personal details saved. Proceeding to Career Selection...\n```")
            await asyncio.sleep(0.3)
            await select_career(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        else:
            await send_dm(user, "```text\n[RESET] Let's enter the details again.\n```")
            await select_personal_details(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
    except Exception as e:
        logger.error(f"Error in personal details selection: {e}")
        if user_id in creation_sessions and char_id in creation_sessions[user_id]:
            del creation_sessions[user_id][char_id]
        await send_dm(user, "```text\n[ERROR] Character creation failed. Please try again with /createcharacter.\n```")
        raise

async def select_career(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
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
                    await start_attr(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
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
            await start_attr(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
            return
        await send_dm(user, "```text\n[ERROR] Invalid input. Enter a number, dN, or pN.\n```")

async def start_attr(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
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
                    await assign_skills(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
                    return
                elif confirm.content.strip().upper() == "N":
                    await send_dm(user, """```text\n[RESET] Let's enter the values again.\n```""")
                    for attr in attr_order:
                        setattr(char.attributes, attr.lower(), 2)
                    points_remaining = 6
                    current_attr_index = 0
                    break
                else:
                    await send_dm(user, "```text\n[ERROR] Please enter Y or N\n```")
                    continue
            continue
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

async def assign_skills(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
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
    available_skills = [s for s in all_skills if s not in key_skills]
    while True:
        skill_list = '\n'.join(f"[{i+1}] {s}" for i, s in enumerate(available_skills) if getattr(char.skills, s.lower().replace(" ", "_")) == 0)
        await send_dm(user, f"""```text\nEnter general skills to assign (comma/space-separated indices, up to {points_remaining}):\nType B to go back to key skills.\n{skill_list}\n```""")
        if points_remaining <= 0:
            break
        msg = await wait_for_user_message(user)
        cmd = msg.content.strip().upper()
        if cmd == "B" or cmd == "BACK":
            await assign_skills(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
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
        await select_talent(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        return
    else:
        await send_dm(user, "```text\n[RESET] Let's reassign skills.\n```")
        for skill in key_skills + available_skills:
            skill_attr = skill.lower().replace(" ", "_")
            setattr(char.skills, skill_attr, 0)
        await assign_skills(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        return

async def select_talent(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
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
        if char.career in data_manager.get_playergen()["Talents"] and talent_name in data_manager.get_playergen()["Talents"][char.career]:
            description = data_manager.get_playergen()["Talents"][char.career][talent_name]["description"]
        elif "General" in data_manager.get_playergen()["Talents"] and talent_name in data_manager.get_playergen()["Talents"]["General"]:
            description = data_manager.get_playergen()["Talents"]["General"][talent_name]["description"]
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
        await select_agenda(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        return

async def select_agenda(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
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
        await select_gear(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        return

async def select_gear(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No career found in session. Please start over with /createcharacter.\n```")
        return
    char = creation_sessions[user_id][char_id]
    gear_list = careers[char.career]["starting_gear"]
    gear_pairs = get_paired_gear(gear_list)
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
        first_pair_index = (choice - 1) // 2
        first_pair = gear_pairs[first_pair_index]
        remaining_gear = []
        for i, item in enumerate(gear_list):
            if item == first_item:
                continue
            if item in first_pair:
                continue
            remaining_gear.append(item)
        menu = ["```text", ">> GEAR SELECTION <<"]
        menu.append(f"You have selected {get_article_for_item(first_item)} as your first item. Please select the second piece of gear for your {char.career}.")
        menu.append(f"\nNOTE: Because you have selected {get_article_for_item(first_item)}, you are precluded via game rules from also selecting {get_article_for_item(first_pair[0] if first_item == first_pair[1] else first_pair[1])}, which has been removed from the list of remaining selectable items below.")
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
                await select_signature_item(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
                return
            else:
                await send_dm(user, "[RESET] Let's select gear again.")
                char.inventory = Inventory()
                break

async def select_signature_item(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
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
        await apply_starting_cash_and_finalize(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
        return

async def apply_starting_cash_and_finalize(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
    if user_id not in creation_sessions or char_id not in creation_sessions[user_id]:
        await send_dm(user, "```text\n[ERROR] No character in progress. Please start over with /createcharacter.\n```")
        return
    char = creation_sessions[user_id][char_id]
    formula = careers[char.career]["cash"]
    amt = DiceRoll.roll(formula)
    char.cash = amt
    await send_dm(user, "[OK] Cash assigned. Proceeding to final review...")
    await finalize_character(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger, finalstep=True)

async def finalize_character(user, char_id: str, send_dm, wait_for_user_message, creation_sessions, logger, finalstep=False):
    careers = data_manager.get_playergen()["Careers"]
    user_id = str(user.id)
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
            weapon_names = {w.name for w in find_weapon_by_name.__globals__['all_weapon_items']}
            new_inventory = []
            for item in char.inventory.items:
                if item.name in weapon_names:
                    from models.weapon_item import WeaponItem
                    if not isinstance(item, WeaponItem):
                        canonical = next((w for w in find_weapon_by_name.__globals__['all_weapon_items'] if w.name == item.name), None)
                        if canonical:
                            char.weapons.append(canonical)
                        else:
                            char.weapons.append(WeaponItem(name=item.name))
                    else:
                        char.weapons.append(item)
                else:
                    new_inventory.append(item)
            char.inventory.items = new_inventory
            data_manager.characters[user_id][char_id] = char
            if not data_manager.primary_characters.get(user_id):
                logger.debug(f"Setting {char.name} as primary character for user {user_id}")
                data_manager.primary_characters[user_id] = char_id
            data_manager.save_characters()
            logger.debug(f"Characters after save: {data_manager.characters}")
            logger.debug(f"Primary characters after save: {data_manager.primary_characters}")
            del creation_sessions[user_id][char_id]
            await send_dm(user, """```text\n[OK] Character creation complete!\nYour character has been saved and is ready for use.\n```""")
            return
        elif choice == "0":
            await send_dm(user, """```text\nAre you sure you want to restart character creation? This will erase all progress. (Y/N)\n```""")
            confirm = await wait_for_user_message(user)
            if confirm.content.strip().upper() == "Y":
                del creation_sessions[user_id][char_id]
                await send_dm(user, """```text\n[RESET] Starting character creation over...\n```""")
                await select_career(user, char_id, send_dm, wait_for_user_message, creation_sessions, logger)
                return
            else:
                continue
        elif finalstep and choice in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            await edit_section(user, char_id, choice, send_dm, wait_for_user_message, creation_sessions, logger)
            continue
        else:
            await send_dm(user, "```text\n[ERROR] Please enter a valid option.\n```")
            continue

async def edit_section(user, char_id, section, send_dm, wait_for_user_message, creation_sessions, logger):
    await send_dm(user, f"```text\n[EDIT] Section {section} editing not yet implemented. Returning to summary...\n```")
    return

# Each function should take send_dm, wait_for_user_message, and creation_sessions as arguments, and use them instead of relying on globals.

# ... (functions will be pasted here in the next step) ... 