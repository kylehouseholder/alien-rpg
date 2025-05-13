#!/bin/bash

# Configuration
VULTURE_CONFIDENCE=80
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
REPORTS_DIR="code_analysis/reports"
VULTURE_OUT="$REPORTS_DIR/vulture_report.txt"
RUFF_OUT="$REPORTS_DIR/ruff_report.txt"
USAGE_OUT="$REPORTS_DIR/code_usage_report.txt"
HISTORY_OUT="$REPORTS_DIR/dead_code_history.txt"

# Ensure reports directory exists
mkdir -p "$REPORTS_DIR"

# Files that are part of the game mechanics library
GAME_MECHANICS=(
    "models/weapons.py"
    "models/equipment.py"
    "models/worldbuilding.py"
    "models/armor.py"
    "models/consumables.py"
    "models/medicals.py"
    "models/pharmaceuticals.py"
)

# Files that are explicitly marked for future use
FUTURE_USE=(
    "models/character.py"
    "models/items.py"
)

# Create a temporary file for filtered results
TEMP_FILE=$(mktemp)

# Add timestamp to history
echo "=== Dead Code Analysis Run: $TIMESTAMP ===" >> "$HISTORY_OUT"
echo "----------------------------------------" >> "$HISTORY_OUT"

echo "🔍 Running Vulture (excluding venv/)..."
vulture . --exclude "venv" --min-confidence $VULTURE_CONFIDENCE > "$TEMP_FILE"

# Generate usage report with timestamp
echo "📊 Code Usage Report - Generated: $TIMESTAMP" > "$USAGE_OUT"
echo "==========================================" >> "$USAGE_OUT"

# Check for game mechanics files
echo -e "\n🎮 Game Mechanics Library:" >> "$USAGE_OUT"
for file in "${GAME_MECHANICS[@]}"; do
    if [ -f "$file" ]; then
        echo "  $file - Part of game mechanics library" >> "$USAGE_OUT"
        # Remove from Vulture report
        grep -v "$file" "$TEMP_FILE" > "$VULTURE_OUT"
        mv "$VULTURE_OUT" "$TEMP_FILE"
    fi
done

# Check for future use files
echo -e "\n🔮 Planned Future Usage:" >> "$USAGE_OUT"
for file in "${FUTURE_USE[@]}"; do
    if [ -f "$file" ]; then
        echo "  $file - Marked for future implementation" >> "$USAGE_OUT"
        # Remove from Vulture report
        grep -v "$file" "$TEMP_FILE" > "$VULTURE_OUT"
        mv "$VULTURE_OUT" "$TEMP_FILE"
    fi
done

# Add timestamp and summary statistics to Vulture report
echo "📊 Vulture Analysis Report - Generated: $TIMESTAMP" > "$VULTURE_OUT"
echo "=============================================" >> "$VULTURE_OUT"
cat "$TEMP_FILE" >> "$VULTURE_OUT"
echo -e "\n📊 Summary:" >> "$VULTURE_OUT"
echo "Total unused items found: $(wc -l < "$TEMP_FILE")" >> "$VULTURE_OUT"
echo "Files with unused code: $(grep -c "^[^:]*:" "$TEMP_FILE")" >> "$VULTURE_OUT"

# Add summary to history
echo "Vulture Findings:" >> "$HISTORY_OUT"
echo "  - Total unused items: $(wc -l < "$TEMP_FILE")" >> "$HISTORY_OUT"
echo "  - Files with unused code: $(grep -c "^[^:]*:" "$TEMP_FILE")" >> "$HISTORY_OUT"

echo "🔍 Running Ruff (unused imports and vars)..."
ruff check . --select F401,F841 > "$TEMP_FILE"

# Add timestamp and summary to Ruff report
echo "📊 Ruff Analysis Report - Generated: $TIMESTAMP" > "$RUFF_OUT"
echo "===========================================" >> "$RUFF_OUT"
cat "$TEMP_FILE" >> "$RUFF_OUT"
echo -e "\n📊 Summary:" >> "$RUFF_OUT"
echo "Total unused imports/vars found: $(grep -c "^[^:]*:" "$TEMP_FILE")" >> "$RUFF_OUT"

# Add Ruff summary to history
echo "Ruff Findings:" >> "$HISTORY_OUT"
echo "  - Total unused imports/vars: $(grep -c "^[^:]*:" "$TEMP_FILE")" >> "$HISTORY_OUT"
echo -e "\n" >> "$HISTORY_OUT"

# Cleanup
rm "$TEMP_FILE"

echo "✅ Analysis complete."
echo "📁 Reports saved to:"
echo "  - $VULTURE_OUT"
echo "  - $RUFF_OUT"
echo "  - $USAGE_OUT"
echo "  - $HISTORY_OUT"
