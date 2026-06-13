from database.db_manager import DatabaseManager
from database.init_spells import add_spells
from database.init_dnd_class import add_dnd_classes 
from database.init_weapons import add_weapons


def init_database():

    db = DatabaseManager("dnd_database.db")
    db.setup_tables()

    add_spells(db)
    add_dnd_classes(db)
    add_weapons(db)

    