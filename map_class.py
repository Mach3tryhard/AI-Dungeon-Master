from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
import random

class MapClass:
    def __init__(self,size=(7,7),matrix=None):

        self.mapping = {
            'enemy': "E",
            'player': "P",
            'barrier': "1",
            'empty': "0",
            'wood': "2",
            'stone': "1",
            'npc': "N"
        }

        self.size = size
        if matrix:
            self.size = (len(matrix), len(matrix[0]))
            self.base_map = [[str(cell) for cell in row] for row in matrix]
        else:
            self.size = size
            self.base_map = [["0" for _ in range(size[1])] for _ in range(size[0])]
            for i in range(size[0]):
                for j in range(size[1]):
                    if i == 0 or i == size[0] - 1 or j == 0 or j == size[1] - 1:
                        self.base_map[i][j] = self.mapping['barrier']
        
        self.full_map = [["0" for _ in range(self.size[1])] for _ in range(self.size[0])]


    def mapData(self,enemies: dict, npcs: dict,player : Entity):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.full_map[i][j] = self.base_map[i][j]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if player.position == (j, i):
                    self.full_map[i][j] = self.mapping['player']
                else:
                    for e in enemies.values():
                        if getattr(e, 'health', 0) > 0 and getattr(e, 'position', None) == (j, i):
                            self.full_map[i][j] = self.mapping['enemy']
                    for n in npcs.values():
                        if getattr(n, 'position', None) == (j, i):
                            self.full_map[i][j] = self.mapping['npc']

    def getAdjacentFreeTile(self, target_x: int, target_y: int, enemies: dict):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = target_x + dx, target_y + dy
                
                if 0 <= ny < len(self.base_map) and 0 <= nx < len(self.base_map[0]):
                    if self.base_map[ny][nx] == self.mapping['empty']:
                        
                        occupied = False
                        for e in enemies.values():
                            if getattr(e, 'health', 0) > 0 and getattr(e, 'position', None) == (nx, ny):
                                occupied = True
                                break
                        
                        if not occupied:
                            return (nx, ny)
        return None