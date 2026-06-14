from database.db_manager import DatabaseManager

def add_dnd_classes(db: "DatabaseManager"):
    db.add_dnd_class(
        name="Wizard",
        primary_stat="INT",
        health=10,        
        cantrips=["Fire Bolt", "Magic Missle"],
        spells = ["Magic Touch"],
        abilities= [],
        skill_proficiencies=["Arcana", "History"],
        max_cantrips=3,
        max_spells=5,
        spell_slots=2,
        weapon_proficiencies=[],
        spellcaster=True
    )

    db.add_dnd_class(
        name="Paladin",
        primary_stat="WIS",
        health=15,
        cantrips=["Smite"],
        spells = [],
        abilities=[],
        skill_proficiencies=["Religion", "History"],
        weapon_proficiencies=["Hammer"],
        max_cantrips=2,
        max_spells=3,
        spell_slots=2,
        spellcaster=True
    )
    db.add_dnd_class (
        name="Fighter",
        primary_stat="STR",
        health=15,
        skill_proficiencies=["Atheltics", "Persuasion"],
        weapon_proficiencies=["Sword"],
        spells = [],
        abilities=[],
        cantrips=[],
        max_cantrips=0,
        max_spells=0,
        spell_slots=0,
        spellcaster=False
    )
    # DEFAULT ENEMY CLASS
    db.add_dnd_class(
        name="normal",
        primary_stat="STR",
        health=10,
        cantrips=[],
        spells = [],
        abilities=[],
        skill_proficiencies=[],
        weapon_proficiencies=[],
        max_cantrips=0,
        max_spells=0,
        spell_slots=0,
        spellcaster=False
    )

    