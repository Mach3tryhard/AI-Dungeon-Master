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
        

    def attack(self, attacker: 'Entity', target: 'Entity'):
        dice = Dice()
        d20_roll = dice.roll('1d20')

        #exit if attack doesn't hit
        if d20_roll < target.ac:
            print(f"{attacker.name} attacks {target.name} with {self.name} but misses!")
            return -1
        
        damage = dice.roll(self.damage_roll)
        damage += attacker.get_modifier(attacker.dnd_class.primary_stat) 

        #damage is dealt in engine.py 
        # target.take_damage(damage, self.damage_type)
        return damage
    