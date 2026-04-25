from dnd_class import *
from spell_class import *
from utils import *

class Entity:
    def __init__(self, dnd_class: DNDClass, name: str, stats: dict, speed: int = 5, position: tuple = (0, 0), inventory: list = None):
        self.dnd_class = dnd_class
        self.stats = stats
        self.name = name
        self.health = dnd_class.health
        self.spells = dnd_class.spells
        self.speed = speed
        self.level = 1
        self.position = position
        self.inventory = inventory if inventory is not None else []
        self.influenced = False #True if charmed/intimidated/persuaded etc. 

    @property
    def ac(self):
        return 10 + self.get_modifier("DEX")

    def get_modifier(self, stat: str):
        return (self.stats[stat] - 10) // 2 
    
    def take_damage(self, damage:int, damage_type: str):
        if self.health >= damage:
            self.health -= damage
        else:
            self.health = 0

    def heal(self, amount: int):
        self.health += amount
        if self.health > self.dnd_class.health:
            self.health = self.dnd_class.health

    #TODO: add skill checks. how should this be implemented?
    # each skill requires a certain stat...
    def skill_check(self, skill: str):
        pass
    
