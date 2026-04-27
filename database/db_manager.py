import sqlite3

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

        self.conn.commit()

    def add_dnd_class(self,  name: str, primary_stat: str, health: int, abilities: list, cantrips: list,
                      skill_proficiencies: list, weapon_proficiencies: list, max_cantrips: int,
                      max_spells: int, spell_slots: int, spellcaster: bool):
        
        abilities_str = ", ".join(abilities) if abilities else ""
        cantrips_str = ", ".join(cantrips) if cantrips else ""
        skill_proficiencies_str = ", ".join(skill_proficiencies) if skill_proficiencies else ""
        weapon_proficiencies_str = ", ".join(weapon_proficiencies) if weapon_proficiencies else ""
        spellcaster_int = 1 if spellcaster else 0

        self.cursor.execute("""
            INSERT OR IGNORE INTO dnd_classes (name, primary_stat, health, 
                            abilities, cantrips, skill_proficiencies, 
                            weapon_proficiencies, max_cantrips, max_spells, 
                            spell_slots, spellcaster)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, primary_stat, health, 
              abilities_str, cantrips_str, skill_proficiencies_str, 
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

    def close(self):
        self.conn.close()