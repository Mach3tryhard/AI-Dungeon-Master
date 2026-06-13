from database.db_manager import DatabaseManager

def add_spells(db: "DatabaseManager"):
    db.add_spell(
        name="Fire Bolt",
        spell_type="damage",
        spell_range=10,
        level=0,
        dice_roll="1d10",
        damage_type="fire"
    )
    db.add_spell(
        name="Ice Touch",
        spell_type="damage",
        spell_range=15,
        level=0,
        dice_roll="2d8",
        damage_type="Ice"
    )
    db.add_spell(
        name="Fire Ball",
        spell_type="damage",
        spell_range=20,
        area = 9,
        level=2,
        dice_roll="3d10",
        damage_type="fire"
    )
    db.add_spell(
        name="Lightning Bolt",
        spell_type="damage",
        spell_range=30,
        level=1,
        dice_roll="2d8",
        damage_type="Lightning"
    )   
    db.add_spell(
        name="Magic Missle",
        spell_type="damage",
        spell_range=15,
        level=0,
        dice_roll="1d8",
        damage_type="Magic"
    )
    db.add_spell(
        name="Smite",
        spell_type="damage",
        spell_range=5,
        level=0,
        dice_roll="1d8",
        damage_type="Holy"
    )
    db.add_spell(
        name="Apprentice's Heal",
        spell_type="healing",
        spell_range=30,
        level=0,
        dice_roll="2d4",
    )