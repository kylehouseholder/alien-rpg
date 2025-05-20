# Session management for character creation moved from main.py

from typing import Dict
from models.character import Character

# creation_sessions: Dict[str, Dict[str, Character]]
creation_sessions: Dict[str, Dict[str, Character]] = {}

# Add any session management helpers here as needed. 