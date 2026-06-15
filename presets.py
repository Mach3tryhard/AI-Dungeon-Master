CLASS_STATS = {
    "Barbarian": {"STR": 15, "DEX": 13, "CON": 14, "INT": 8,  "WIS": 10, "CHA": 12, "HP": 15},
    "Bard":      {"STR": 8,  "DEX": 14, "CON": 13, "INT": 12, "WIS": 10, "CHA": 15, "HP": 10},
    "Cleric":    {"STR": 14, "DEX": 10, "CON": 13, "INT": 8,  "WIS": 15, "CHA": 12, "HP": 11},
    "Druid":     {"STR": 10, "DEX": 12, "CON": 14, "INT": 13, "WIS": 15, "CHA": 8,  "HP": 10},
    "Fighter":   {"STR": 15, "DEX": 13, "CON": 14, "INT": 10, "WIS": 12, "CHA": 8,  "HP": 12},
    "Monk":      {"STR": 10, "DEX": 15, "CON": 13, "INT": 10, "WIS": 14, "CHA": 8,  "HP": 10},
    "Paladin":   {"STR": 15, "DEX": 10, "CON": 13, "INT": 8,  "WIS": 12, "CHA": 14, "HP": 12},
    "Ranger":    {"STR": 10, "DEX": 15, "CON": 14, "INT": 12, "WIS": 13, "CHA": 8,  "HP": 12},
    "Rogue":     {"STR": 8,  "DEX": 15, "CON": 13, "INT": 14, "WIS": 10, "CHA": 12, "HP": 10},
    "Sorcerer":  {"STR": 8,  "DEX": 13, "CON": 14, "INT": 10, "WIS": 12, "CHA": 15, "HP": 8},
    "Warlock":   {"STR": 8,  "DEX": 13, "CON": 14, "INT": 12, "WIS": 10, "CHA": 15, "HP": 10},
    "Wizard":    {"STR": 8,  "DEX": 13, "CON": 14, "INT": 15, "WIS": 12, "CHA": 10, "HP": 8},
}

RACE_BONUSES = {
    "Human":      {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1},
    "Elf":        {"STR": 0, "DEX": 2, "CON": 0, "INT": 1, "WIS": 0, "CHA": 0},
    "Dwarf":      {"STR": 2, "DEX": 0, "CON": 2, "INT": 0, "WIS": 0, "CHA": 0},
    "Halfling":   {"STR": 0, "DEX": 2, "CON": 0, "INT": 0, "WIS": 0, "CHA": 1},
    "Dragonborn": {"STR": 2, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 1},
    "Gnome":      {"STR": 0, "DEX": 0, "CON": 0, "INT": 2, "WIS": 0, "CHA": 0},
    "Half-Elf":   {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 2},
    "Half-Orc":   {"STR": 2, "DEX": 0, "CON": 1, "INT": 0, "WIS": 0, "CHA": 0},
    "Tiefling":   {"STR": 0, "DEX": 0, "CON": 0, "INT": 1, "WIS": 0, "CHA": 2},
}

STARTING_EQUIPMENT = {
    "Barbarian": {"gold": 15, "weapon": {"name": "Greataxe", "damage_roll": "1d12", "damage_type": "slashing", "range": 1, "level": 1}},
    "Bard":      {"gold": 40, "weapon": {"name": "Rapier", "damage_roll": "1d8", "damage_type": "piercing", "range": 1, "level": 1}},
    "Cleric":    {"gold": 35, "weapon": {"name": "Mace", "damage_roll": "1d6", "damage_type": "bludgeoning", "range": 1, "level": 1}},
    "Druid":     {"gold": 25, "weapon": {"name": "Scimitar", "damage_roll": "1d6", "damage_type": "slashing", "range": 1, "level": 1}},
    "Fighter":   {"gold": 50, "weapon": {"name": "Longsword", "damage_roll": "1d8", "damage_type": "slashing", "range": 1, "level": 1}},
    "Monk":      {"gold": 10, "weapon": {"name": "Martial Arts", "damage_roll": "1d4", "damage_type": "bludgeoning", "range": 1, "level": 1}},
    "Paladin":   {"gold": 45, "weapon": {"name": "Warhammer", "damage_roll": "1d8", "damage_type": "bludgeoning", "range": 1, "level": 1}},
    "Ranger":    {"gold": 30, "weapon": {"name": "Longbow", "damage_roll": "1d8", "damage_type": "piercing", "range": 5, "level": 1}},
    "Rogue":     {"gold": 40, "weapon": {"name": "Dagger", "damage_roll": "1d4", "damage_type": "piercing", "range": 1, "level": 1}},
    "Sorcerer":  {"gold": 20, "weapon": {"name": "Fire Bolt", "damage_roll": "1d10", "damage_type": "fire", "range": 4, "level": 1}},
    "Warlock":   {"gold": 25, "weapon": {"name": "Eldritch Blast", "damage_roll": "1d10", "damage_type": "force", "range": 4, "level": 1}},
    "Wizard":    {"gold": 25, "weapon": {"name": "Quarterstaff", "damage_roll": "1d6", "damage_type": "bludgeoning", "range": 1, "level": 1}},
}

CLASS_TRAITS = {
    "Barbarian": ["Rage", "Unarmored Defense"],
    "Bard":      ["Bardic Inspiration", "Spellcasting"],
    "Cleric":    ["Divine Domain", "Spellcasting"],
    "Druid":     ["Druidic", "Spellcasting"],
    "Fighter":   ["Second Wind", "Action Surge"],
    "Monk":      ["Martial Arts", "Unarmored Defense"],
    "Paladin":   ["Divine Sense", "Lay on Hands"],
    "Ranger":    ["Favored Enemy", "Natural Explorer"],
    "Rogue":     ["Sneak Attack", "Cunning Action"],
    "Sorcerer":  ["Sorcerous Origin", "Spellcasting"],
    "Warlock":   ["Otherworldly Patron", "Pact Magic"],
    "Wizard":    ["Arcane Recovery", "Spellcasting"],
}

BACKGROUNDS = [
    "Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", 
    "Guild Artisan", "Hermit", "Noble", "Outlander", "Sage", "Sailor", "Soldier", "Urchin"
]