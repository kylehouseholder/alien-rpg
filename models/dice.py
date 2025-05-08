from typing import List, Tuple, Union
import re
import random

class DiceRoll:
    """Handles parsing and rolling of dice expressions"""
    
    DICE_PATTERN = re.compile(r'^(\d+)d(\d+)(?:\s*x\s*(\d+))?$')
    
    @staticmethod
    def parse_expression(expression: str) -> Tuple[int, int, int]:
        """Parse a dice expression like '1d6' or '2d8 x 100'
        Returns (number_of_dice, dice_sides, multiplier)"""
        match = DiceRoll.DICE_PATTERN.match(expression.strip())
        if not match:
            raise ValueError(f"Invalid dice expression: {expression}")
            
        num_dice = int(match.group(1))
        sides = int(match.group(2))
        multiplier = int(match.group(3)) if match.group(3) else 1
        
        return num_dice, sides, multiplier
    
    @staticmethod
    def roll(expression: str) -> int:
        """Roll dice based on expression and return result"""
        num_dice, sides, multiplier = DiceRoll.parse_expression(expression)
        result = sum(random.randint(1, sides) for _ in range(num_dice))
        return result * multiplier
        
    @staticmethod
    def roll_with_details(expression: str) -> Tuple[int, List[int]]:
        """Roll dice and return both final result and individual rolls"""
        num_dice, sides, multiplier = DiceRoll.parse_expression(expression)
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        result = sum(rolls) * multiplier
        return result, rolls 