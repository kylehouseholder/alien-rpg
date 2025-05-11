@dataclass
class EquipmentItem(Item):
    name: str
    cost: int
    encumbrance: Optional[float] = 0
    description: Optional[str] = None
    skill_bonus: Optional[Dict[str, int]] = None
    usage_tags: List[str] = field(default_factory=list)  # e.g., ["diagnostic", "communications"]
    slot: Optional[str] = None  # e.g., "hand", "wrist", "implant"

