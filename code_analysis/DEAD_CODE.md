# Dead Code Management

This document tracks decisions about potentially unused code in the codebase.

## Directory Structure

```
code_analysis/
├── analyze-unused.sh    # Main analysis script
├── DEAD_CODE.md        # This documentation file
└── reports/            # Generated analysis reports
    ├── vulture_report.txt
    ├── ruff_report.txt
    ├── code_usage_report.txt
    └── dead_code_history.txt
```

## Report Files

The dead code analysis system generates several reports in the `reports/` directory:

1. `vulture_report.txt` - Detailed report of potentially unused code
2. `ruff_report.txt` - Report of unused imports and variables
3. `code_usage_report.txt` - Context about why certain code is kept
4. `dead_code_history.txt` - Historical record of all analysis runs

Each report includes a timestamp of when it was generated, and the history file maintains a record of all analysis runs over time.

## Code Categories

### Game Mechanics Library
These files contain game mechanics and data that are part of the core game systems:
- `models/weapons.py` - Weapon definitions and mechanics
- `models/equipment.py` - Equipment and item definitions
- `models/worldbuilding.py` - World generation and system mechanics
- `models/armor.py` - Armor and protection mechanics
- `models/consumables.py` - Consumable items and effects
- `models/medicals.py` - Medical items and healing mechanics
- `models/pharmaceuticals.py` - Drug and chemical effects

### Planned Future Implementation
These files contain code that is currently unused but planned for future features:
- `models/character.py` - Character creation and management
- `models/items.py` - Item system and inventory management

## Review Process

1. Weekly dead code analysis is run using `code_analysis/analyze-unused.sh`
2. Findings are categorized:
   - Safe to Remove - Code that is truly unused and not part of any planned features
   - Needs Review - Code that might be used in ways not detected by static analysis
   - Keep (with justification) - Code that is part of planned features or game mechanics
3. Decisions are documented here
4. All analysis runs are recorded in `reports/dead_code_history.txt`

## Current Status

### Safe to Remove
- List items here as they are identified

### Needs Review
- List items here as they are identified

### Keep
- List items here with justification

## Notes on Static Analysis Limitations

1. **Dynamic Usage**: Some code may be used through dynamic imports or reflection
2. **Future Implementation**: Code may be unused but planned for future features
3. **Game Mechanics**: Some code may be part of the game mechanics library
4. **Testing**: Code may be used in tests or for debugging purposes

When reviewing dead code reports, consider:
- Is this code part of a planned feature?
- Could this code be used dynamically?
- Is this code part of the game mechanics library?
- Is this code used in tests or debugging?

## History Tracking

The `reports/dead_code_history.txt` file maintains a chronological record of all analysis runs, including:
- Timestamp of each run
- Number of unused items found
- Number of files with unused code
- Number of unused imports and variables

This history helps track:
- Trends in code usage over time
- Impact of code cleanup efforts
- Growth of the codebase
- Effectiveness of the analysis system 