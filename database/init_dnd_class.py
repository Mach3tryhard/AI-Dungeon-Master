from database.db_manager import DatabaseManager

def add_dnd_classes(db: "DatabaseManager"):
    db.add_dnd_class(
        name="Wizard",
        primary_stat="INT",
        health=10,        
        cantrips=["Fire Bolt", "Magic Missle"],
        skill_proficiencies=["Arcana", "History"],
        max_cantrips=3,
        max_spells=5,
        spell_slots=2,
        spellcaster=True
    )

    db.add_dnd_class(
        name="Paladin",
        primary_stat="WIS",
        health=15,
        cantrips=["Smite"],
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
        max_cantrips=0,
        max_spells=0,
        spell_slots=0,
        spellcaster=False
    )

    