import sqlite3

#TODO:
# map_class -> ia din baza de date layoutul matrice aleatoriu
# !location_class -> contine clasa, inamici
# query pentru harta
# query pentru inamici random
# stats random pt NPC
class DatabaseManager:
    def __init__(self, db_name="dnd_database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def setup_tables(self):
        #we first create tables if they don't yet exist

        #dnd class/job table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dnd_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                primary_stat TEXT NOT NULL,
                health INTEGER NOT NULL,
                abilities TEXT,
                cantrips TEXT,
                spells TEXT,
                skill_proficiencies TEXT,
                weapon_proficiencies TEXT,
                max_cantrips INTEGER NOT NULL,
                max_spells INTEGER NOT NULL,
                spell_slots INTEGER NOT NULL,
                spellcaster INTEGER NOT NULL
            )
        """)

        #TODO: consider implementing bufing spells once that is implemented
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                spell_type TEXT NOT NULL,
                spell_range REAL NOT NULL,
                level INTEGER NOT NULL,
                dice_roll TEXT NOT NULL,
                damage_type TEXT,
                area REAL,
                use_count INTEGER                
            )            
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weapons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                primary_stat TEXT NOT NULL,
                dice_roll TEXT NOT NULL,
                range INTEGER NOT NULL,
                level INTEGER NOT NULL,
                damage_type TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS enemies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                creature TEXT NOT NULL,
                dnd_class TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS maps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layout TEXT UNIQUE NOT NULL,
                size_x INTEGER NOT NULL,
                size_y INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dnd_class TEXT NOT NULL
            )
        """)

        self.conn.commit()

    def add_dnd_class(self,  name: str, primary_stat: str, health: int, abilities: list, cantrips: list,
                      spells: list, skill_proficiencies: list, weapon_proficiencies: list, max_cantrips: int,
                      max_spells: int, spell_slots: int, spellcaster: bool):
        
        abilities_str = ", ".join(abilities) if abilities else ""
        cantrips_str = ", ".join(cantrips) if cantrips else ""
        spells_str = ", ".join(spells) if spells else ""
        skill_proficiencies_str = ", ".join(skill_proficiencies) if skill_proficiencies else ""
        weapon_proficiencies_str = ", ".join(weapon_proficiencies) if weapon_proficiencies else ""
        spellcaster_int = 1 if spellcaster else 0

        self.cursor.execute("""
            INSERT OR IGNORE INTO dnd_classes (name, primary_stat, health, 
                            abilities, cantrips, spells, skill_proficiencies, 
                            weapon_proficiencies, max_cantrips, max_spells, 
                            spell_slots, spellcaster)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, primary_stat, health, 
              abilities_str, cantrips_str, spells_str, skill_proficiencies_str, 
              weapon_proficiencies_str, max_cantrips, max_spells, spell_slots, 
              spellcaster_int))
        self.conn.commit()

    def add_spell(self, name: str, spell_type: str, spell_range: float, level: int, dice_roll: str,
                  damage_type: str = None, area: float = None, use_count: int = 0):
        self.cursor.execute("""
            INSERT OR IGNORE INTO spells (name, spell_type, spell_range, level, dice_roll, damage_type, area, use_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, spell_type, spell_range, level, dice_roll, damage_type, area, use_count))
        self.conn.commit()


    def add_map(self, layout: str, size_x: int, size_y: int):
    

        self.cursor.execute("""
            INSERT OR IGNORE INTO maps
            (layout, size_x, size_y)
            VALUES ( ?, ?, ?)
        """, (layout, size_x, size_y))

        self.conn.commit()


    def add_weapon(self, name: str, primary_stat: str, dice_roll: str, range: int, level: int, 
                   damage_type: str = None):
        self.cursor.execute("""
            INSERT OR IGNORE INTO weapons (name, primary_stat, dice_roll, range, level, damage_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, primary_stat, dice_roll, range, level, damage_type))
        self.conn.commit()

    def add_enemy(self, name: str, creature: str, dnd_class: str):
        self.cursor.execute("""
            INSERT OR IGNORE INTO enemies
            (name, creature, dnd_class)
            VALUES (?, ?, ?)
        """, (name, creature, dnd_class))

        self.conn.commit()

    def add_npc(self, name: str, dnd_class: str):
        self.cursor.execute("""
            INSERT OR IGNORE INTO npcs
            (name, dnd_class)
            VALUES (?, ?)
        """, (name, dnd_class))

        self.conn.commit()



    def get_dnd_class(self, name: str) -> dict:
        self.cursor.execute("SELECT * FROM dnd_classes WHERE name = ? COLLATE NOCASE", (name,))
        row = self.cursor.fetchone()
        
        if not row:
            return None

        data = dict(row)
            
        data["abilities"] = data["abilities"].split(", ") if data["abilities"] else []
        data["cantrips"] = data["cantrips"].split(", ") if data["cantrips"] else []
        data["skill_proficiencies"] = data["skill_proficiencies"].split(", ") if data["skill_proficiencies"] else []
        data["weapon_proficiencies"] = data["weapon_proficiencies"].split(", ") if data["weapon_proficiencies"] else []
        data["spellcaster"] = bool(data["spellcaster"])
        return data
    
    def get_spell(self, name: str) -> dict:
        self.cursor.execute("SELECT * FROM spells WHERE name = ? COLLATE NOCASE", (name,))
        row = self.cursor.fetchone()
        
        if not row:
            return None

        data = dict(row)
        return data

    def get_weapon(self, name: str) -> dict:
        self.cursor.execute("SELECT * FROM weapons WHERE name = ? COLLATE NOCASE", (name,))
        row = self.cursor.fetchone()
        
        if not row:
            return None

        data = dict(row)
        return data
    
    def get_map(self) -> dict:
        self.cursor.execute(
            "SELECT * FROM maps ORDER BY RANDOM() LIMIT 1"
        )
        row = self.cursor.fetchone()
        if not row:
            return None

        data = dict(row)

        return data
    
    def get_enemy_by_name(self, name: str) -> dict:
        self.cursor.execute(
            "SELECT * FROM enemies WHERE creature = ? COLLATE NOCASE",
            (name,)
        )

        row = self.cursor.fetchone()

        if not row:
            return None

        data = dict(row)

        return data
    
    def get_enemies_by_creature(self, creature: str) -> list[dict]:
        self.cursor.execute(
            "SELECT * FROM enemies WHERE creature = ? COLLATE NOCASE",
            (creature,)
        )

        rows = self.cursor.fetchall()

        if not rows:
            return []

        return [dict(row) for row in rows]
    
    def get_random_enemy_by_creature(self, creature: str) -> dict:
        self.cursor.execute(
            """
            SELECT *
            FROM enemies
            WHERE creature = ? COLLATE NOCASE
            ORDER BY RANDOM()
            LIMIT 1
            """,
            (creature,)
        )

        row = self.cursor.fetchone()

        if not row:
            return None

        return dict(row)
    
    def get_random_npc(self) -> dict:
        self.cursor.execute(
            "SELECT * FROM npcs ORDER BY RANDOM() LIMIT 1"
        )

        row = self.cursor.fetchone()

        if not row:
            return None

        return dict(row)

    def get_random_enemy(self) -> dict:
        self.cursor.execute(
            "SELECT * FROM enemies ORDER BY RANDOM() LIMIT 1"
        )

        row = self.cursor.fetchone()

        if not row:
            return None

        return dict(row)
    
    def close(self):
        self.conn.close()