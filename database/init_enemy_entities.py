from database.db_manager import DatabaseManager

def add_enemies(db: "DatabaseManager"):
    # Goblins
    db.add_enemy(
        name="Goblin Warrior",
        creature="Goblin",
        dnd_class="normal"
    )


    db.add_enemy(
        name="Goblin Shaman",
        creature="Goblin",
        dnd_class="wizard"
    )

    # Skeletons
    db.add_enemy(
        name="Skeleton Warrior",
        creature="Skeleton",
        dnd_class="normal"
    )


    db.add_enemy(
        name="Skeleton Mage",
        creature="Skeleton",
        dnd_class="wizard"
    )

    # Orcs
    db.add_enemy(
        name="Orc Grunt",
        creature="Orc",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Orc Berserker",
        creature="Orc",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Orc Warlock",
        creature="Orc",
        dnd_class="wizard"
    )

    # Bandits
    db.add_enemy(
        name="Bandit",
        creature="Human",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Bandit Leader",
        creature="Human",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Cult Wizard",
        creature="Human",
        dnd_class="wizard"
    )

    # Undead
    db.add_enemy(
        name="Zombie",
        creature="Undead",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Ghoul",
        creature="Undead",
        dnd_class="normal"
    )

    db.add_enemy(
        name="Necromancer",
        creature="Undead",
        dnd_class="wizard"
    )