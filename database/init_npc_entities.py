from database.db_manager import DatabaseManager

def add_npcs(db: "DatabaseManager"):
    # Normal villagers
    db.add_npc(
        name="Thomas Miller",
        dnd_class="normal"
    )

    db.add_npc(
        name="Sarah Baker",
        dnd_class="normal"
    )

    db.add_npc(
        name="John Farmer",
        dnd_class="normal"
    )

    db.add_npc(
        name="Emily Weaver",
        dnd_class="normal"
    )

    db.add_npc(
        name="Robert Merchant",
        dnd_class="normal"
    )

    # Fighters
    db.add_npc(
        name="Marcus Ironhand",
        dnd_class="fighter"
    )

    db.add_npc(
        name="Cedric Stonehelm",
        dnd_class="fighter"
    )

    db.add_npc(
        name="Helga Battleborn",
        dnd_class="fighter"
    )

    db.add_npc(
        name="Garrick Steelblade",
        dnd_class="fighter"
    )

    db.add_npc(
        name="Brom Hammerfist",
        dnd_class="fighter"
    )

    # Wizards
    db.add_npc(
        name="Eldrin Frostweaver",
        dnd_class="wizard"
    )

    db.add_npc(
        name="Selene Moonspell",
        dnd_class="wizard"
    )

    db.add_npc(
        name="Alaric the Wise",
        dnd_class="wizard"
    )

    db.add_npc(
        name="Meridia Starseer",
        dnd_class="wizard"
    )

    db.add_npc(
        name="Thaddeus Blackroot",
        dnd_class="wizard"
    )

    # Paladins
    db.add_npc(
        name="Sir Roland Brightshield",
        dnd_class="paladin"
    )

    db.add_npc(
        name="Lady Elowen Dawnbringer",
        dnd_class="paladin"
    )

    db.add_npc(
        name="Sir Gareth Lightbane",
        dnd_class="paladin"
    )

    db.add_npc(
        name="Dame Victoria Goldheart",
        dnd_class="paladin"
    )

    db.add_npc(
        name="Sir Tristan Oakshield",
        dnd_class="paladin"
    )