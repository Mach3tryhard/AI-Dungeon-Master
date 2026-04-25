from typing import TYPE_CHECKING
from utils import *

if TYPE_CHECKING:
    from entity_class import Entity

class Spell:
    def __init__(self, name: str, spell_range: float, level: int, dice_roll: str):
        self.name = name
        self.spell_range = spell_range
        self.level = level
        self.dice_roll = dice_roll

    def cast(self, caster: 'Entity', target: 'Entity'):
        pass


class damageSpell(Spell):
    def __init__(self, name: str, spell_range: float, level: int, dice_roll: str, damage_type: str, area: float):
        super().__init__(name, spell_range, level, dice_roll)
        self.damage_type = damage_type
        self.area = area #goes sqrt(area) around the initial target

    #TODO: add AOE damage and maybe saving throws
    def cast(self, caster: 'Entity', target: 'Entity'):
        dice = Dice()
        d20_roll = dice.roll('1d20')

        #exit if spell doesn't hit
        if d20_roll < target.ac:
            print(f"{caster.name} casts {self.name} on {target.name} but misses!")
            return
        
        damage = dice.roll(self.dice_roll)
        #each character class has a stat that increases spell damage
        damage += caster.get_modifier(caster.dnd_class.primary_stat) 
        target.take_damage(damage, self.damage_type)
        print(f"{caster.name} casts {self.name} on {target.name} for {damage} {self.damage_type} damage!")
# damageSpell


class healingSpell(Spell):
    def __init__(self, name: str, spell_range: float, level: int, dice_roll: str):
        super().__init__(name, spell_range, level, dice_roll)
    
    def cast(self, caster: 'Entity', target: 'Entity'):
        dice = Dice()
        d20_roll = dice.roll('1d20')

        heal_amount = dice.roll(self.dice_roll)
        heal_amount += caster.get_modifier(caster.dnd_class.primary_stat)
        target.heal(heal_amount)
        print(f"{caster.name} casts {self.name} on {target.name} for {heal_amount} healing!")
    
# healingSpell

class buffingSpell(Spell):
    def __init__(self, name: str, spell_range: float, level: int, dice_roll: str, use_count: int):
        super().__init__(name, spell_range, level, dice_roll)
        self.use_count = use_count
