from typing import TYPE_CHECKING
from utils import *

if TYPE_CHECKING:
    from entity_class import Entity

class Weapon:
    def __init__(self, name, damage_roll: str, damage_type: str, level: int, range: int = 1):
        self.name = name
        self.damage_roll = damage_roll
        self.damage_type = damage_type
        self.level = level
        self.range = range
        

    def attack(self, attacker: 'Entity', target: 'Entity') -> dict:
        dice = Dice()
        d20_roll = dice.roll('1d20')
        
        # Obținem modificatorul. Pentru simplitate, folosim atributul principal al clasei jucătorului
        modifier = attacker.get_modifier(attacker.dnd_class.primary_stat)
        total_attack = d20_roll + modifier

        # Verificăm dacă lovește
        if total_attack < target.ac:
            return {
                "hit": False,
                "d20_roll": d20_roll,
                "total_attack": total_attack,
                "damage": 0,
                "damage_type": self.damage_type
            }
        
        base_damage = dice.roll(self.damage_roll)
        total_damage = max(1, base_damage + modifier) # Asigurăm minimum 1 damage

        return {
            "hit": True,
            "d20_roll": d20_roll,
            "total_attack": total_attack,
            "damage": total_damage,
            "damage_type": self.damage_type
        }
    