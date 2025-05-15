from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from .character import Character

class ActionType(Enum):
    SLOW = "slow"
    FAST = "fast"

@dataclass
class CombatAction:
    """Represents a single combat action that can be taken during a turn"""
    name: str
    action_type: ActionType
    description: str
    prerequisite: Optional[str] = None
    skill_used: Optional[str] = None
    requires_roll: bool = False
    allows_reaction: bool = False

class InitiativeCard:
    """Represents an initiative card drawn at the start of combat"""
    def __init__(self, value: int):
        self.value = value
        self.holder: Optional[Character] = None

class CombatRound:
    """Manages a single round of combat"""
    def __init__(self):
        self.initiative_order: List[InitiativeCard] = []
        self.current_turn_index: int = 0
        self.round_number: int = 1
        
    def add_participant(self, character: Character, initiative_value: int):
        """Add a character to the initiative order"""
        card = InitiativeCard(initiative_value)
        card.holder = character
        self.initiative_order.append(card)
        # Sort by initiative value (lowest to highest)
        self.initiative_order.sort(key=lambda x: x.value)
        
    def get_current_actor(self) -> Optional[Character]:
        """Get the character whose turn it is"""
        if not self.initiative_order:
            return None
        return self.initiative_order[self.current_turn_index].holder
    
    def advance_turn(self) -> bool:
        """Advance to the next turn. Returns True if round is complete."""
        self.current_turn_index += 1
        if self.current_turn_index >= len(self.initiative_order):
            self.current_turn_index = 0
            self.round_number += 1
            return True
        return False

class CombatManager:
    """Manages the overall combat state and actions"""
    def __init__(self):
        self.current_round: Optional[CombatRound] = None
        self.combat_active: bool = False
        self.available_actions: Dict[str, CombatAction] = {
            # --- SLOW ACTIONS ---
            "crawl": CombatAction(
                name="Crawl",
                action_type=ActionType.SLOW,
                description="Move while prone.",
                prerequisite="You are prone"
            ),
            "close_combat_attack": CombatAction(
                name="Close combat attack",
                action_type=ActionType.SLOW,
                description="Attack in close combat.",
                skill_used="close_combat",
                requires_roll=True
            ),
            "shoot_firearm": CombatAction(
                name="Shoot firearm",
                action_type=ActionType.SLOW,
                description="Fire a ranged weapon.",
                prerequisite="Firearm",
                skill_used="ranged_combat",
                requires_roll=True
            ),
            "burst_full_auto": CombatAction(
                name="Burst of full auto fire",
                action_type=ActionType.SLOW,
                description="Fire a burst with a firearm.",
                prerequisite="Firearm",
                skill_used="ranged_combat",
                requires_roll=True
            ),
            "throw_weapon": CombatAction(
                name="Throw weapon",
                action_type=ActionType.SLOW,
                description="Throw a weapon.",
                prerequisite="Thrown weapon",
                skill_used="ranged_combat",
                requires_roll=True
            ),
            "reload": CombatAction(
                name="Reload",
                action_type=ActionType.SLOW,
                description="Reload a firearm.",
                prerequisite="Firearm"
            ),
            "first_aid": CombatAction(
                name="First aid",
                action_type=ActionType.SLOW,
                description="Give first aid to a broken or dying victim.",
                prerequisite="Broken or dying victim",
                skill_used="medical_aid",
                requires_roll=True
            ),
            "stop_panic": CombatAction(
                name="Stop panic",
                action_type=ActionType.SLOW,
                description="Calm a panicking character.",
                prerequisite="Panicking character",
                skill_used="command",
                requires_roll=True
            ),
            "give_orders": CombatAction(
                name="Give orders",
                action_type=ActionType.SLOW,
                description="Give orders to a character who can hear you.",
                prerequisite="Character who can hear you",
                skill_used="command",
                requires_roll=True
            ),
            "persuade": CombatAction(
                name="Persuade",
                action_type=ActionType.SLOW,
                description="Persuade an opponent who can hear you.",
                prerequisite="Your opponent can hear you",
                skill_used="manipulation",
                requires_roll=True
            ),
            "use_signature_item": CombatAction(
                name="Use signature item",
                action_type=ActionType.SLOW,
                description="Use your signature item.",
                prerequisite="Signature Item"
            ),
            "climb_into_space_suit": CombatAction(
                name="Climb into space suit",
                action_type=ActionType.SLOW,
                description="Climb into a space suit.",
                prerequisite="Space suit",
                skill_used="mobility",
                requires_roll=True
            ),

            # --- FAST ACTIONS ---
            "run": CombatAction(
                name="Run",
                action_type=ActionType.FAST,
                description="Run (no enemy at Engaged range).",
                prerequisite="No enemy at Engaged range"
            ),
            "move_through_door": CombatAction(
                name="Move through door/hatch",
                action_type=ActionType.FAST,
                description="Move through a door or hatch."
            ),
            "get_up": CombatAction(
                name="Get up",
                action_type=ActionType.FAST,
                description="Get up from prone.",
                prerequisite="You are prone"
            ),
            "draw_weapon": CombatAction(
                name="Draw weapon",
                action_type=ActionType.FAST,
                description="Draw or ready a weapon."
            ),
            "block_attack": CombatAction(
                name="Block attack",
                action_type=ActionType.FAST,
                description="Block an attack in close combat.",
                prerequisite="Attacked in close combat",
                skill_used="close_combat",
                requires_roll=True
            ),
            "pick_up_item": CombatAction(
                name="Pick up item",
                action_type=ActionType.FAST,
                description="Pick up an item."
            ),
            "shove": CombatAction(
                name="Shove",
                action_type=ActionType.FAST,
                description="Shove an enemy at Engaged range.",
                prerequisite="Enemy at Engaged range",
                skill_used="close_combat",
                requires_roll=True
            ),
            "grapple_attack": CombatAction(
                name="Grapple attack",
                action_type=ActionType.FAST,
                description="Attack a grappled opponent.",
                prerequisite="You've grappled an opponent",
                skill_used="close_combat",
                requires_roll=True
            ),
            "retreat": CombatAction(
                name="Retreat",
                action_type=ActionType.FAST,
                description="Retreat from an enemy at Engaged range.",
                prerequisite="Enemy at Engaged range",
                skill_used="mobility",
                requires_roll=True
            ),
            "aim": CombatAction(
                name="Aim",
                action_type=ActionType.FAST,
                description="Aim with a ranged weapon.",
                prerequisite="Ranged weapon"
            ),
            "seek_cover": CombatAction(
                name="Seek cover",
                action_type=ActionType.FAST,
                description="Seek cover in the same zone.",
                prerequisite="Cover in same zone"
            ),
            "assume_overwatch": CombatAction(
                name="Assume overwatch position",
                action_type=ActionType.FAST,
                description="Assume overwatch with a ranged weapon.",
                prerequisite="Ranged weapon"
            ),
            "start_engine": CombatAction(
                name="Start engine",
                action_type=ActionType.FAST,
                description="Start a vehicle engine.",
                prerequisite="Vehicle"
            ),
            "grab_the_wheel": CombatAction(
                name="Grab the wheel",
                action_type=ActionType.FAST,
                description="Grab the wheel of a vehicle.",
                prerequisite="Vehicle"
            ),
            "drive": CombatAction(
                name="Drive",
                action_type=ActionType.FAST,
                description="Drive a vehicle.",
                prerequisite="Vehicle",
                skill_used="piloting",
                requires_roll=True
            ),
            "enter_exit_vehicle": CombatAction(
                name="Enter/exit vehicle",
                action_type=ActionType.FAST,
                description="Enter or exit a vehicle.",
                prerequisite="Vehicle"
            ),
            "use_item": CombatAction(
                name="Use item",
                action_type=ActionType.FAST,
                description="Use an item (varies).",
                prerequisite="Varies",
                skill_used="Varies"
            ),
        }
    
    def start_combat(self, participants: List[Character], initiative_values: List[int]):
        """Start a new combat with the given participants and their initiative values"""
        self.combat_active = True
        self.current_round = CombatRound()
        
        for character, initiative in zip(participants, initiative_values):
            self.current_round.add_participant(character, initiative)
    
    def end_combat(self):
        """End the current combat"""
        self.combat_active = False
        self.current_round = None
    
    def get_available_actions(self, character: Character) -> List[CombatAction]:
        """Get the list of actions available to a character"""
        return list(self.available_actions.values())
    
    def can_perform_action(self, character: Character, action: CombatAction) -> bool:
        """Check if a character can perform the given action"""
        if not self.combat_active or not self.current_round:
            return False
            
        current_actor = self.current_round.get_current_actor()
        if current_actor != character:
            return False
            
        # Additional checks could be added here (e.g., checking if character has required items)
        return True 