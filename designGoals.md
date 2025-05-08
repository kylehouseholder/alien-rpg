# ALIEN RPG BOT README
### A turn-based narrative Discord bot for hosting immersive, AI-assisted Alien TTRPG sessions.
- The bot facilitates character creation, state tracking, and dynamic GM narration via an LLM.



## **I. OVERVIEW**
This bot is designed to provide a seamless TTRPG experience using OpenAI’s GPT model to emulate a Game Master (GM).

Players interact with the bot through Discord in a shared channel, taking turns while the bot maintains world state, player conditions, and narrative flow.

Private interactions (e.g., inventory management or merchant dialogues) are supported via DM.


## **II. CORE FEATURES**
* Turn-based player system with controlled narrative pacing.
* Character creation and inventory systems.
* LLM-powered GM for scene narration and creative storytelling.
* Contextual memory and per-turn state saving.
* Immersive session wakeups via narrative prompts.
* Private sub-context interactions (e.g., merchants, secrets).
* Admin override tools and privileged commands.



## **III. GAMEPLAY FLOW**

### 1. **Session Wakeup**

  The LLM receives prior session state and all stored narrative memory (saved in structured JSON format). This includes:

  - **Character progress:** States of players, inventory, and active character attributes (health, skills, etc.).

  - **World state:** Key locations, NPC statuses, active quests, and current game progression.

  - **Combat status:** If there was any ongoing combat, the LLM receives detailed data about enemies, the battlefield, health statuses, and any ongoing conditions (e.g., poison, bleeding).

  The LLM processes all received data and generates a narrative prompt to reintroduce players to the session. This prompt should offer a sense of continuity, reminding players of their last actions and setting up a new narrative direction.

### 2. **Player Turns**
Players act sequentially within a shared channel. The order is determined either by initiative (in combat) or at the discretion of the bot for non-combat tasks (exploration, interaction).

For each turn:

* **Action Interpretation:** Players’ actions are parsed by the bot. The LLM determines if the action is valid (checking things like inventory, proximity, or active abilities).

* **Action Result:** The LLM processes the action, and the results are calculated (such as damage dealt, skill checks, or item usage). The result is then presented in the shared channel and is stored in the session state (JSON).

* **State Updates:** After each action, the game state is updated. For example, inventory changes, character health updates, or enemy stats are all saved to JSON. This helps keep track of ongoing changes and provides information for the next turn.

### 3. **Event Handling**

The system handles different types of events based on context:

* **Combat:** The bot triggers combat-specific logic, such as roll checks (for damage, defense, and status effects). The LLM must have access to all enemy stats, weapons, and player abilities during combat.

* **Exploration:** For non-combat actions (such as moving around, interacting with NPCs, or searching the environment), the bot checks the context, retrieves relevant world data (e.g., location description, available objects), and updates the session state.

* **Travel:** Travel events trigger changes in the world map, enemy encounters, or arrival at new locations. These actions need to be handled by the bot and can involve new combat or NPC interaction.

* **Context-Specific** JSON Loading:

For each type of event (combat, exploration, travel), the bot loads the appropriate JSON data and executes corresponding actions based on current game mechanics (combat damage calculations, NPC dialogues, item usage).

### 4. **Narrative Control**

Admins can intervene during gameplay and change the course of events by:

- Overriding ongoing scenes or narrative prompts.

- Pausing sessions when needed (such as for unexpected breaks or game state resets).

- Adjusting the world state manually, e.g., introducing new events, enemies, or locations.

- Triggering game resets or "force-restarts" when necessary, such as in case of crashes or bugs.

Admin commands may need to be prefixed to avoid confusion with player actions (e.g., /admin pause, /admin change-world).

### 5. **Session Conclusion**

At the conclusion of a session, a full save snapshot is taken. This includes:

- Player states (current health, inventory, quest progression).

- World state (current map, completed quests, NPC interactions).

- Combat status (if a fight is unfinished, the bot should store that information for future reference).

**Narrative Wrap-Up:** The LLM generates a session summary or narrative wrap-up. This summary can be stored for future use and optionally presented to players as a recap of what happened, what was accomplished, and where things stand for future sessions.

**Session Closure:** At the end of each session, context should be saved in a way that allows easy and seamless retrieval during the next session. This includes character and world state, as well as any unsolved narrative threads that might be picked up where they left off.


## **IV. STATE MANAGEMENT**
* **Data Format**: The game state is managed using structured Python objects and serialized to JSON format for flexibility and readability. Each file represents a discrete part of the game world or player data, such as `players.json`, `world.json`, or temporary `combat_session.json`.

* **Per-Turn Saves**: After every player action, the bot saves all relevant state to disk. This includes:

  * Character status (health, stress, inventory, conditions)
  * Scene-specific context (active enemies, environment status)
  * Combat snapshots, travel progress, or puzzle stages

* **Storage Philosophy**:

  * **Persistent files** represent stable elements (characters, explored areas).
  * **Temporary files** track evolving scenes (combat turns, DM events).
  * Temporary files are archived or purged at event conclusion.

* **Example Structure**:

  * `players/{player_id}.json`
  * `scenes/{scene_id}/context.json`
  * `combat/{encounter_id}/snapshot_turn_3.json`

* **Crash Recovery**:

  * The latest per-turn snapshot allows near-instant recovery from crashes or server downtime.
  * A restart triggers the LLM to generate a reentry narrative based on last known state (e.g., collision event, static interruption).

* **Selective Context Feeding**:

  * The LLM is only given essential context based on interaction scope (e.g., for combat: characters, weapons, enemies; for travel: location, NPCs, hazards).
  * Token-saving strategies include shortening narrative history, flattening object trees, and trimming attributes irrelevant to the current scene.

### **Serialized JSON Example** (combat turn state):

```json
{
  "turn": 4,
  "players": [
    {
      "id": "young",
      "hp": 6,
      "stress": 2,
      "weapon": "m41a"
    },
    {
      "id": "doc",
      "hp": 4,
      "condition": "burned"
    }
  ],
  "enemies": [
    {
      "type": "xenomorph",
      "variant": "drone",
      "hp": 8,
      "status": [
        "aggressive",
        "injured leg"
      ]
    }
  ],
  "scene": {
    "location": "airlock_bay",
    "features": [
      "low_gravity",
      "flickering_lights"
    ]
  },
  "log": [
    "Young fires his pulse rifle, hitting the xenomorph.",
    "Doc stumbles behind a crate."
  ]
}
```

### **Example Python Stub**:
```py
class Player:
  def __init__(self, name, hp, stress):
    self.name = name
    self.hp = hp
    self.stress = stress

  def to_dict(self):
    return {"name": self.name, "hp": self.hp, "stress": self.stress}

  @staticmethod
  def from_dict(data):
    return Player(data["name"], data["hp"], data["stress"])
```

* **LLM Interface Strategy**:

  * The state file is reformatted into bullet-point summaries or inline descriptions before being passed as part of the LLM prompt.
  * Files are not dumped raw into the prompt.
  * Wherever possible, summaries are cached and reused between turns.

* **Scene Transitioning**:

  * Exiting combat archives the combat snapshot and loads exploration state.
  * Scene files track ambient status and unscripted changes (e.g., fire spreading, power outage).


## **V. LLM INTERACTION DESIGN**
### **System Prompt**:

  * A detailed and customized system prompt is used to establish the LLM's role as a GM.
  * This prompt enforces tone, genre-appropriate vocabulary, and awareness of key rules.
  * Includes behavioral expectations (e.g., avoid player favoritism, handle pacing).

      ### Example:
      - You are the Game Master (GM) for a sci-fi horror tabletop RPG. You are responsible for narrating events, interpreting player actions, and describing the world. Remain in character as a vivid, immersive narrator.

      - Use the provided JSON data to understand the current game state. Do not summarize the data; instead, interpret it to describe the scene and outcomes. If a player action is ambiguous or invalid, respond with a narrative that reflects confusion or consequence—never break character.

      - Only respond with narration, dialogue, or descriptive outcomes of player actions. Do not ask questions unless a decision point is necessary.

      #### _**Current game state includes:**_
      - **Active Location:** Derelict Cargo Bay, filled with flickering lights, overturned crates, and low oxygen warnings.

      - **Player Character:** Lt. Reyes (HP: 6/10), wielding an M314 Pulse Rifle (Ammo: 14), wearing Light Combat Armor.

      - **Enemies:** One hostile Xenomorph (HP: 7/12), currently stalking the catwalk above the players.

      - **Recent Turn:** Reyes moved into cover behind a steel crate after taking a glancing hit from the Xenomorph's claw.

      - **Current Action:** Reyes attempts to aim and shoot at the Xenomorph using the pulse rifle.

        Respond with a vivid narration of the result of this action, including emotional cues, environmental feedback, and enemy behavior.
### **Source State .json**
```json
{
  "location": {
    "name": "Derelict Cargo Bay",
    "description": "Flickering lights, overturned crates, and low oxygen warnings. The air smells of rust and ozone.",
    "features": [
      "catwalk overhead",
      "steel crates for cover",
      "sparking conduit in far corner"
    ],
    "status_effects": [
      "low_oxygen"
    ]
  },
  "players": [
    {
      "id": "lt_reyes",
      "name": "Lt. Reyes",
      "health": 6,
      "max_health": 10,
      "inventory": [
        {
          "name": "M314 Pulse Rifle",
          "type": "weapon",
          "ammo": 14,
          "attributes": {
            "damage": "2d6",
            "range": "medium",
            "accuracy_bonus": 2
          }
        },
        {
          "name": "Light Combat Armor",
          "type": "armor",
          "defense": 2
        }
      ],
      "status_effects": [
        "in_cover"
      ]
    }
  ],
  "enemies": [
    {
      "name": "Xenomorph",
      "variant": "Standard Drone",
      "health": 7,
      "max_health": 12,
      "location": "catwalk",
      "traits": [
        "stealthy",
        "aggressive",
        "acidic_blood"
      ],
      "status_effects": [
        "stalking"
      ]
    }
  ],
  "turn_context": {
    "active_player": "lt_reyes",
    "current_action": "shoot_enemy",
    "target": "xenomorph",
    "weapon_used": "M314 Pulse Rifle",
    "cover_bonus": true
  },
  "previous_turn": {
    "action": "move_to_cover",
    "result": "success",
    "description": "Reyes dove behind a steel crate after dodging a claw swipe."
  }
}
```


* **Session Context**:

  * Each turn includes a rolling context of the last 1–3 player actions and outcomes.
  * The LLM is also given high-level summaries of current objectives, emotional tone, character status, and scene dynamics.
  * Certain conditions (e.g., stress, hunger, injuries) are flagged as tags or bullet points.

* **Structured Prompts**:

  * Data is provided in sections: "Player Action", "Current Scene Summary", "World State Tags", "Known NPCs", etc.
  * These headers help the LLM reason modularly and avoid distraction from irrelevant details.

* **Subprompting (Optional)**:

  * Admins can send hidden messages via DM to guide or correct the LLM mid-session.
  * These include nudges like "focus on paranoia" or "introduce malfunctioning equipment".

* **Command Suggestion & Automation**:

  * The LLM may suggest commands the bot can parse for automation (e.g., `/use_item` or `/end_turn`).
  * These are proposed only when natural to the narrative and usually follow a successful action or discovery.

* **Responsiveness to Roleplay**:

  * If a player inputs prose (e.g., "Reyes glares at the dark corridor"), the LLM is encouraged to embellish and deepen the atmosphere.
  * If input is mechanical ("I shoot the vent"), the LLM balances tactical and narrative consequences.

* **Handling Conflicts & Interruptions**:

  * When more than one player interacts simultaneously, the LLM follows established turn rules unless the scene context allows interrupt resolution.
  * In some cases, interruptions are mediated via skill checks (e.g., reflex, wit) to preserve fairness.

* **Recovery Narratives**:

  * Upon bot crash or session restore, the LLM generates a transition narrative.
  * This may include environmental disturbances or new story hooks ("an impact shakes the hull...").

## **VI. PRIVATE VS PUBLIC CHANNELS**
* **Public**: All game narrative and turns occur here.
* **Private (DM)**: Used for:

  * Character creation.
  * Inventory or private decisions.
  * Solo dialogues (e.g., merchant interaction).
  * Admin actions (subprompting, scene override).


## **VII. ADMIN TOOLS**
* Force turn/pass.
* Pause/resume gameplay.
* Inject narrative or trigger scene change.
* Restart/resume LLM context.
* Toggle AFK mode or NPC replacement.


## **VIII. CONTEXT STRATEGY**
### **1. Context Size Management**

To avoid overwhelming the LLM’s token limits, context should be maintained in small, modular chunks. For example:

  * **Player State:** A small data set with current health, inventory, and known abilities.

  * **World State:** Each location should have a brief description, the list of NPCs, and key items or features.

  * **Combat State:** Only the current combatants and the last few actions taken should be kept in the active context.

### **2. Context Pruning and Summarization**

The LLM should be capable of summarizing lengthy events in a concise format. For example:

  * **Summarized Combat:** After a major battle, the LLM summarizes: "The battle with the alien was hard-fought, but the party emerged victorious, though Player1 suffered a minor injury."

  * **World Events:** "The crew successfully repaired the ship's engine, and they now venture deeper into the alien ship."

This ensures that memory is efficiently stored, reducing the burden on the LLM’s token limit, while retaining critical information to guide future interactions.

### **3. Dynamic Context Injection**

For specific interactions, the LLM can “inject” detailed context on-the-fly. For example, when interacting with a unique NPC or facing an uncommon scenario, the LLM can dynamically load the necessary context and present it to the player.


## **IX. SESSION WAKEUPS**
Narrative wakeup prompts provide seamless transition from offline to active state. These are generated from saved JSON state + recent narrative trends.

*Example:*

> Young's cryo capsule opened first, and despite the clouded eyes from the deep rest he could see stars moving past at sublight speed...

## **X. GAME RULES & OUT-OF-TURN ACTIONS**
* Off-turn actions (e.g., interruptions) are resolved via stat-based rolls.
* Failed interruptions may result in narrative consequences.
* Flexible GM discretion guided by character traits (e.g., wit, reflex).


## **XI. COMBAT SNAPSHOTS** - Overview
### *Combat Start:*

- Load player states, weapons, items.
- Load enemy variant stats.
- Save full encounter snapshot.

### *Per Turn:*
- Log damage, special effects, movement.
- Lookup traits, item usage, resistance.
- Append to combat history.

### *End:*
- Archive snapshot.
- Return to travel/exploration state.

## Combat Snapshot File
Pay special attention to the `combat_log` at the end.

```json
{
  "location": {
    "name": "Orbital Station Theta-7",
    "room": "Hydroponics Bay",
    "features": ["broken irrigation pipes", "dense plant overgrowth", "flickering overhead lights", "scattered chemical tanks"],
    "environmental_effects": ["low_visibility", "slippery_floor"]
  },
  "turn": 6,
  "combat_active": true,
  "players": [
    {
      "id": "capt_young",
      "name": "Captain Elias Young",
      "class": "Officer",
      "health": 5,
      "max_health": 10,
      "position": "southwest corner",
      "status_effects": ["burned_leg", "suppressed"],
      "inventory": [
        {
          "id": "service_pistol",
          "name": "M9 Service Pistol",
          "ammo": 5
        },
        {
          "id": "stim_pack",
          "name": "Combat Stim Pack",
          "uses": 1
        }
      ],
      "traits": ["leadership", "tactical_insight"],
      "last_action": "Issued evasive maneuver order to team"
    },
    {
      "id": "dr_kovacs",
      "name": "Dr. Mira Kovacs",
      "class": "Scientist",
      "health": 9,
      "max_health": 9,
      "position": "central basin",
      "status_effects": [],
      "inventory": [
        {
          "id": "bio_scanner",
          "name": "Portable Bio-Scanner",
          "charge": 2
        },
        {
          "id": "stun_baton",
          "name": "Shock Baton",
          "charge": 1
        }
      ],
      "traits": ["xeno_biology", "precision"],
      "last_action": "Scanned enemy for weak points"
    },
    {
      "id": "reyes",
      "name": "Sgt. Marco Reyes",
      "class": "Marine",
      "health": 6,
      "max_health": 12,
      "position": "eastern walkway",
      "status_effects": ["light_bleeding"],
      "inventory": [
        {
          "id": "smartgun",
          "name": "M56 Smartgun",
          "ammo": 20
        },
        {
          "id": "frag_grenade",
          "name": "Fragmentation Grenade",
          "fuse_set": true
        }
      ],
      "traits": ["heavy_weapons", "battle_hardened"],
      "last_action": "Fired suppression burst at alien"
    }
  ],
  "enemies": [
    {
      "id": "xeno_stalker_01",
      "name": "Stalker-class Xenomorph",
      "variant": "Vortex Spine",
      "health": 11,
      "max_health": 15,
      "status_effects": ["minor_injury", "adaptive"],
      "position": "north ventilation shaft",
      "traits": ["stealth", "acid_blood", "predictive_dodge"],
      "current_behavior": "circling through vents, adapting to weapon fire",
      "last_action": "Disengaged from Reyes and disappeared into vent system"
    }
  ],
  "combat_log": [
    "Turn 1: Reyes landed 3 hits on the Stalker, forcing it to retreat.",
    "Turn 2: Young drew fire, distracting the Stalker momentarily.",
    "Turn 3: Kovacs used Bio-Scanner to identify carapace weak points.",
    "Turn 4: The alien countered with a tail swipe, burning Young’s leg with acidic spray.",
    "Turn 5: Reyes fired suppression burst, damaging pipes and lowering visibility.",
    "Turn 6: Kovacs shouted a weak point location. Young issued a squad-wide evasion order. Alien retreated to the north vent shaft."
  ],
  "environmental_state": {
    "visibility": "poor",
    "hazards": ["exposed wiring", "acid corrosion near southwest crates"],
    "ambient_conditions": {
      "temperature": "cold",
      "lighting": "intermittent",
      "structural_integrity": "unstable"
    }
  }
}
```

## **XII. CRASH RECOVERY**
If the session is interrupted or the bot crashes:

* Restore from last saved state.
* LLM generates post-recovery narrative (e.g., "the ship shakes from unexpected impact...").


## **XIII. FUTURE IDEAS**
* Dialogue-based crafting, lockpicking, or repairs.
* Character-aligned AI stand-ins during AFK.
* Expanding session memory using embeddings.
* Multi-location scene stacks for simultaneous player arcs.

---

\== END ==