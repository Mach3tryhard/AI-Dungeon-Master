from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
import random

class MapClass:
    def __init__(self,size=(7,7)):
        self.size = size
        rows, cols = size
        self.base_map = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                    self.base_map[i][j] = 1

    def mapData(self,enemies,player) -> str:
        lines = []
        for y, row in enumerate(self.base_map):
            line_chars = []
            for x, tile in enumerate(row):
                char = str(tile)
                if player.position == (x, y):
                    char = "P"
                else:
                    for e in enemies.values():
                        if getattr(e, 'health', 0) > 0 and getattr(e, 'position', None) == (x, y):
                            char = "E"
                            break
                line_chars.append(char)
            lines.append(" ".join(line_chars))
        return "\n".join(lines)

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