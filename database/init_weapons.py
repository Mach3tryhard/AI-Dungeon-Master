from database.db_manager import DatabaseManager

def add_weapons(db: "DatabaseManager"):
    db.add_weapon(
        name="Long Sword",
        primary_stat="STR",
        dice_roll="1d8",
        range = 2,
        level = 0,
        damage_type="Slashing"
    )
    db.add_weapon(
        name="Heavy Hammer",
        primary_stat="STR",
        dice_roll="1d12",
        range = 1,
        level = 0,
        damage_type="Bludgeoning"
    )
    db.add_weapon(
        name="Dagger",
        primary_stat="DEX",
        dice_roll="1d4",
        range = 1,
        level = 0,
        damage_type="Piercing"
    )
    db.add_weapon(
        name="Claymore",
        primary_stat="STR",
        dice_roll="2d8",
        range = 2,
        level = 0,
        damage_type="Slashing"
    )
    db.add_weapon(
        name="Spear",
        primary_stat="DEX",
        dice_roll="1d8",
        range = 2,
        level = 0,
        damage_type="Piercing"
    )
    db.add_weapon(
        name="Weak Bat",
        primary_stat="DEX",
        dice_roll="1d4",
        range = 1,
        level = 0,
        damage_type="Bludgeoning"
    )