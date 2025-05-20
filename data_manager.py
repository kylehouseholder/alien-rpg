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

# ==============================
# Alien RPG Data Manager
# ==============================

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
                        gear_list = char_data.get("Gear") or char_data.get("Inventory") or []
                        for gear_item in gear_list:
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