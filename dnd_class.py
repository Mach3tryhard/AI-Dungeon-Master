from spell_class import *
class DNDClass:
    def __init__(self, name: str = "", primary_stat: int = "", health: int = 0, 
                 skill_proficiencies = None, weapon_proficiencies = None,
                 abilites = None, cantrips = None, max_cantrips = 0, 
                 spells=None, max_spells=0, spell_slots=0):
        self.name = name
        self.primary_stat = primary_stat
        self.health = health
        self.skill_proficiencies = skill_proficiencies if skill_proficiencies is not None else []
        self.weapon_proficiencies = weapon_proficiencies if weapon_proficiencies is not None else []
        self.abilites = abilites if abilites is not None else []
        self.cantrips = cantrips if cantrips is not None else []
        self.max_cantrips = max_cantrips
        self.spells = spells if spells is not None else []
        self.max_spells = max_spells
        self.spell_slots = spell_slots
        
    

