from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
import random

class MapClass:
    def __init__(self,size=(7,7)):
        self.size = size
        self.base_map = [["0" for _ in range(size[1])] for _ in range(size[0])]

        self.mapping = {
            'enemy': "E",
            'player': "P",
            'barrier': "1",
            'empty': "0",
            'wood': "2",
            'stone': "1",
            'npc': "N"
        }

        for i in range(size[0]):
            for j in range(size[1]):
                if i == 0 or i == size[0] - 1 or j == 0 or j == size[1] - 1:
                    self.base_map[i][j] = self.mapping['barrier']

    def mapData(self,enemies,player):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if player.position == (i, j):
                    self.base_map[i][j] = self.mapping['player']
                else:
                    for e in enemies.values():
                        if getattr(e, 'health', 0) > 0 and getattr(e, 'position', None) == (i, j):
                            self.base_map[i][j] = self.mapping['enemy']

    def getAdjacentFreeTile(self, target_x: int, target_y: int):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = target_x + dx, target_y + dy
                
                if 0 <= ny < len(self.base_map) and 0 <= nx < len(self.base_map[0]):
                    if self.base_map[ny][nx] == 0:
                        occupied = False
                        for e in self.enemies.values():
                            if getattr(e, 'health', 0) > 0 and getattr(e, 'position', None) == (nx, ny):
                                occupied = True
                                break
                        
                        if not occupied:
                            return (nx, ny)
        return None