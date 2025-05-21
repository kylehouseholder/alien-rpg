import json
import os
import datetime
import copy
import logging
from typing import Dict, Optional
from models.character import Character, Attributes, Skills
from models.items import Item, ConsumableItem, Inventory

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Remove all handlers associated with the root logger object (to avoid duplicate log lines)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
# Set up logger to only output to console (not to scripts/bot.log)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Use whole seconds only in the timestamp
formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.handlers = [console_handler]

# ==============================
# Alien RPG Data Manager
# ==============================

LOG_PATH = os.path.join(os.path.dirname(__file__), "scripts", "bot.log")

def log_event(msg: str):
    logger.info(msg)

class DataManager:
    def __init__(self):
        self.CHARACTER_FILE = "characters.json"
        self.PLAYERGEN_FILE = "data/playerGenData.json"
        self.characters: Dict[str, Dict[str, Character]] = {}  # user_id -> {char_id -> Character}
        self.players: Dict[str, Dict] = {}  # user_id -> player info
        self.playergen: Dict = {}
        
        if not os.path.exists(self.CHARACTER_FILE):
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump({"characters": {}, "players": {}}, f)
                
        self.reload_all()
    
    def reload_all(self):
        logger.info(f"Reloading all data files.")
        self.reload_characters()
        self.reload_playergen()
    
    def reload_characters(self):
        try:
            logger.info(f"Loading characters from {os.path.abspath(self.CHARACTER_FILE)}")
            with open(self.CHARACTER_FILE, "r") as f:
                data = json.load(f)
                self.players = data.get("players", {})  # Ensure players is always loaded
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
                        # Convert inventory (flatten any legacy nested dicts)
                        inventory = Inventory()
                        gear_list = char_data.get("Inventory") or []
                        for gear_item in gear_list:
                            # Flatten any nested 'name' dicts
                            d = gear_item
                            while isinstance(d.get('name'), dict):
                                d = d['name']
                            if 'quantity' in d and any(word in d['name'].lower() for word in ["pills", "rounds", "doses"]):
                                inventory.add_item(ConsumableItem(**d))
                            else:
                                inventory.add_item(Item(**d))
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
            logger.error(f"Error loading characters file: {e}")
            self.characters = {}
            self.players = {}
    
    def reload_playergen(self):
        try:
            logger.info(f"Loading playergen from {os.path.abspath(self.PLAYERGEN_FILE)}")
            with open(self.PLAYERGEN_FILE, "r") as f:
                self.playergen = json.load(f)
        except Exception as e:
            logger.error(f"Error loading playergen: {e}")
            self.playergen = {}
    
    def get_playergen(self) -> Dict:
        """Get the playergen data"""
        return self.playergen
    
    def save_characters(self):
        try:
            abs_path = os.path.abspath(self.CHARACTER_FILE)
            logger.info(f"Saving characters to {abs_path}")
            # Load existing usernames from the file if present
            existing_players = {}
            if os.path.exists(self.CHARACTER_FILE):
                with open(self.CHARACTER_FILE, "r") as f:
                    try:
                        existing_data = json.load(f)
                        existing_players = existing_data.get("players", {})
                    except Exception:
                        existing_players = {}
            # Build players section
            players = {}
            for user_id, user_chars in self.characters.items():
                # Use existing username if present, else fallback to user_id
                username = existing_players.get(user_id, {}).get("name", user_id)
                # Build characters list
                char_list = [ {cid: char.name} for cid, char in user_chars.items() ]
                player_entry = {
                    "name": username,
                    "characters": char_list
                }
                # Add primary_character if present
                if self.players.get(user_id, {}).get("primary_character"):
                    player_entry["primary_character"] = self.players[user_id]["primary_character"]
                players[user_id] = player_entry
            data = {
                "characters": {
                    user_id: {
                        char_id: copy.deepcopy(char.to_json())
                        for char_id, char in user_chars.items()
                    }
                    for user_id, user_chars in self.characters.items()
                },
                "players": players
            }
            with open(self.CHARACTER_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving characters: {e}")
    
    def get_characters(self) -> Dict[str, Dict[str, Character]]:
        return self.characters
    
    def get_user_characters(self, user_id: str) -> Dict[str, Character]:
        return self.characters.get(user_id, {})

    def get_primary_character(self, user_id: str) -> Optional[Character]:
        """Get a user's primary character"""
        if user_id not in self.players:
            return None
        primary_info = self.players[user_id].get('primary_character')
        if not primary_info:
            return None
        char_id = primary_info.get('char_id')
        if char_id:
            return self.characters.get(user_id, {}).get(char_id)
        return None
    
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
            self.players[user_id]['primary_character'] = {'char_id': char_id}
            self.save_characters()
            logger.debug(f"Set primary character for user {user_id} to {char_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting primary character: {e}")
            return False

    def delete_character(self, user_id: str, char_id: str) -> bool:
        """Delete a character for a user. Update primary_characters and save."""
        try:
            if user_id not in self.characters or char_id not in self.characters[user_id]:
                return False
            del self.characters[user_id][char_id]
            # If this was the primary character, pick a new one if any remain
            if self.players.get(user_id, {}).get('primary_character', {}).get('char_id') == char_id:
                remaining = list(self.characters[user_id].keys())
                if remaining:
                    self.players[user_id]['primary_character'] = {'char_id': remaining[0]}
                else:
                    del self.players[user_id]['primary_character']
            self.save_characters()
            return True
        except Exception as e:
            logger.error(f"Error deleting character: {e}")
            return False

data_manager = DataManager() 