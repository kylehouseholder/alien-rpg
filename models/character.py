from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .items import Inventory, Item, ConsumableItem, ClothingItem, ArmorItem, SuitItem, AccessoryItem
from .dice import DiceRoll
from .weapon_item import WeaponItem
from .wearables import WearableLoadout

@dataclass
class Attributes:
    strength: int = 2
    agility: int = 2
    wits: int = 2
    empathy: int = 2

@dataclass
class Skills:
    heavy_machinery: int = 0
    stamina: int = 0
    close_combat: int = 0
    mobility: int = 0
    piloting: int = 0
    ranged_combat: int = 0
    observation: int = 0
    comtech: int = 0
    survival: int = 0
    manipulation: int = 0
    command: int = 0
    medical_aid: int = 0

@dataclass
class Character:
    """Represents a player character in the game, with inventory, loadout, and weapons separated."""
    id: str
    name: str
    career: str
    gender: str = ""
    age: int = 0
    attributes: Attributes = field(default_factory=Attributes)
    skills: Skills = field(default_factory=Skills)
    talent: str = ""
    agenda: str = ""
    inventory: Inventory = field(default_factory=Inventory)
    signature_item: str = ""
    cash: int = 0
    loadout: Optional[WearableLoadout] = None  # Equipped wearables
    weapons: List[WeaponItem] = field(default_factory=list)  # Equipped weapons
    
    @classmethod
    def create_new(cls, char_id: str, name: str) -> 'Character':
        """Create a new character with default values"""
        return cls(
            id=char_id,
            name=name,
            career="",
            gender="",
            age=0,
            attributes=Attributes(),
            skills=Skills(),
            inventory=Inventory(),
            loadout=WearableLoadout(),
            weapons=[]
        )
    
    @classmethod
    def from_json(cls, char_id: str, data: Dict) -> 'Character':
        """Create a character from JSON data. Handles both complete and partial data."""
        # Start with default values
        char = cls(
            id=char_id,
            name=data.get('Name', char_id),  # Use ID as name if not provided
            career=data.get('Career', ""),
            gender=data.get('Gender', ""),
            age=data.get('Age', 0),
            attributes=Attributes(),
            skills=Skills(),
            inventory=Inventory(),
            loadout=WearableLoadout(),
            weapons=[]
        )
        
        # Update attributes if provided
        if 'Attributes' in data and isinstance(data['Attributes'], dict):
            attr_data = {k.lower(): v for k, v in data['Attributes'].items()}
            # Only update valid attributes
            valid_attrs = {'strength', 'agility', 'wits', 'empathy'}
            attr_data = {k: v for k, v in attr_data.items() if k in valid_attrs}
            for attr, value in attr_data.items():
                setattr(char.attributes, attr, value)
            
        # Update skills if provided
        if 'Skills' in data and isinstance(data['Skills'], dict):
            skill_data = {k.lower(): v for k, v in data['Skills'].items()}
            # Only update valid skills
            valid_skills = {
                'heavy_machinery', 'stamina', 'close_combat', 'mobility',
                'piloting', 'ranged_combat', 'observation', 'comtech',
                'survival', 'manipulation', 'command', 'medical_aid'
            }
            skill_data = {k: v for k, v in skill_data.items() if k in valid_skills}
            for skill, value in skill_data.items():
                setattr(char.skills, skill, value)
            
        # Update other fields if provided
        char.talent = data.get('Talent', char.talent)
        char.agenda = data.get('Agenda', char.agenda)
        char.signature_item = data.get('Signature Item', char.signature_item)
            
        # Handle cash with dice roll if needed
        cash_value = data.get('Cash', char.cash)
        if isinstance(cash_value, str) and 'd' in cash_value:
            char.cash = DiceRoll.roll(cash_value)
        elif isinstance(cash_value, (int, str)):
            char.cash = int(cash_value)
            
        # Handle gear if provided
        if 'Gear' in data and isinstance(data['Gear'], list):
            for item in data['Gear']:
                if isinstance(item, str):
                    if 'doses' in item.lower():
                        # Handle items with random quantities
                        name = item.split('doses')[-1].strip()
                        dice_expr = item.split('doses')[0].strip()
                        char.inventory.add_item(ConsumableItem(
                            name=name,
                            dice_expression=dice_expr
                        ))
                    else:
                        char.inventory.add_item(Item(name=item))
                elif isinstance(item, dict):
                    for name in item:
                        char.inventory.add_item(Item(name=name))
                        
        # Load loadout and weapons if present
        if 'Loadout' in data and data['Loadout']:
            char.loadout = WearableLoadout.from_dict(data['Loadout'])
        if 'Weapons' in data:
            # TODO: implement weapon loading if needed
            pass
            
        return char
    
    def to_json(self) -> Dict:
        """Convert character to JSON format, including inventory, loadout, and weapons."""
        # Helper to serialize WearableLoadout
        def serialize_loadout(loadout):
            if not loadout:
                return None
            return loadout.to_dict()
        # Helper to serialize weapons
        def serialize_weapons(weapons):
            return [vars(w) for w in weapons]
        return {
            'Name': self.name,
            'Career': self.career,
            'Gender': self.gender,
            'Age': self.age,
            'Attributes': {
                'Strength': self.attributes.strength,
                'Agility': self.attributes.agility,
                'Wits': self.attributes.wits,
                'Empathy': self.attributes.empathy
            },
            'Skills': {
                k.title(): v for k, v in self.skills.__dict__.items()
            },
            'Talent': self.talent,
            'Agenda': self.agenda,
            'Inventory': [vars(item) for item in self.inventory.items],
            'Signature Item': self.signature_item,
            'Cash': self.cash,
            'Loadout': serialize_loadout(self.loadout),
            'Weapons': serialize_weapons(self.weapons)
        }