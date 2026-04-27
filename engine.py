from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
from map_class import MapClass
import random

class GameEngine:
    def __init__(self):
        self.story_log = ["The journey begins..."]
        self.game_time_seconds = 0
        self.chat_log = []
        
        self.needs_story_update = False
        self.needs_map_update = False
        self.needs_sheet_update = False
        self.needs_equipment_update = False
        self.needs_sheet_update = False
        self.is_thinking = False

        self.map_class = MapClass((7,7))
        
        # CREAM JUCATORUL
        fighter_class = DNDClass(name="Fighter", primary_stat="STR", health=12)
        self.player = Entity (
            dnd_class=fighter_class,
            stats={"STR": 16, "DEX": 14, "CON": 15, "INT": 9, "WIS": 11, "CHA": 13},
            name="Galdor the Brave",
            position= (1,1),
            inventory= ["Longsword", "Shield", "Health Potion"],
        )

        # CREAM UN INAMIC
        goblin_class = DNDClass(name="Monster", primary_stat="DEX", health=15)
        goblin = Entity(dnd_class=goblin_class, name="Goblin", stats={"STR": 8, "DEX": 14, "CON": 10, "INT": 10, "WIS": 8, "CHA": 8},position=(3,3))
        self.enemies = {goblin.name.lower(): goblin}

    def add_story(self, text: str):
        self.story_log.append(text)

    def tick(self):
        self.game_time_seconds += 1
        self.map_class.mapData(self.enemies, self.player)
    
    def process_action(self, intent: dict) -> str:
        action = intent.get("action")
        target_name = intent.get("target")

        action_map = {
            "attack": lambda: self.action_attack(target_name),
            "talk": lambda: self.action_talk(target_name),
        }

        if action in action_map:
            return action_map[action]()
        
        return "Player performed a non-mechanical action. Just narrate it normally."

    # --- FUNCȚII PENTRU ACȚIUNILE JUCĂTORULUI ---

    def auto_approach(self, target) -> tuple[bool, str]:
        px, py = self.player.position
        tx, ty = target.position
        distance = max(abs(px - tx), abs(py - ty))
        
        if distance <= 1:
            return True, ""
            
        free_tile = map_class.getAdjacentFreeTile(tx, ty)
        if free_tile:
            self.player.position = free_tile
            self.needs_map_update = True
            return True, f"Player moved next to {target.name}. "
        else:
            return False, f"Cannot reach {target.name} because all adjacent spaces are blocked."

    def action_attack(self, target_name: str) -> str:
        if not target_name:
            return "Player attempted to attack but specified no valid target."
        
        target = self.enemies.get(target_name.lower())
        if not target:
            return f"Player swung at {target_name}, but it is not here."
            
        if target.health <= 0:
            return f"Player tried to attack {target.name}, but it is already dead."

        reached_target, move_narrative = self.auto_approach(target)
        if not reached_target:
            return f"Attack failed. {move_narrative}"
        
        damage = random.randint(1, 8) + self.player.get_modifier("STR")
        target.take_damage(damage, "slashing")
        
        result = move_narrative + f"Player attacked {target.name}. Hit for {damage} damage. "
        if target.health <= 0:
            result += f"{target.name} died."
        else:
            result += f"{target.name} has {target.health} HP left."
        
        self.needs_sheet_update = True 
        self.needs_map_update=True
        return result

    def action_talk(self, target_name: str) -> str:
        if not target_name:
            return "Player said something to the open air."
            
        target = self.enemies.get(target_name.lower())
        if not target:
            return f"Player tried to talk to {target_name}, but they aren't here."
            
        reached_target, move_narrative = self.auto_approach(target)
        if not reached_target:
            return f"Talk failed. {move_narrative}"
                
        return move_narrative + f"Player said something to {target.name}. The NPC listened."