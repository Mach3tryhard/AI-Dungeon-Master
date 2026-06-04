from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
from map_class import MapClass
from utils import Dice
from weapon_class import Weapon
from inventory_class import Inventory
import random

class GameEngine:
    def __init__(self):
        self.story_log = ["The journey begins..."]
        self.game_time_seconds = 0
        self.chat_log = []
        self.in_combat = False

        self.map_class = MapClass((20,20))
        self.current_location_name = "forest"
        
        self.visited_locations = {} 
        self.visited_locations[self.current_location_name] = {
            "name": self.current_location_name,
            "matrix": self.map_class.base_map
        }

        self.needs_story_update = False
        self.needs_map_update = False
        self.needs_sheet_update = False
        self.needs_equipment_update = False
        self.needs_sheet_update = False
        self.is_thinking = False
        
        # --- VECTORII GLOBALI ---
        self.global_enemies = []
        self.global_npcs = []
        self.quests = {}

        iron_sword = Weapon(
            name="Iron Sword", 
            damage_roll="1d8", 
            damage_type="slashing",
            level=1, 
            range=1
        )
        
        inventory_default = Inventory(items=[iron_sword])

        # --- JUCATORUL ---
        fighter_class = DNDClass(name="Fighter", primary_stat="STR", health=12)
        self.player = Entity(
            dnd_class=fighter_class,
            stats={"STR": 16, "DEX": 14, "CON": 15, "INT": 9, "WIS": 11, "CHA": 13},
            name="Galdor",
            position=(1, 1),
            location=self.current_location_name,
            inventory=inventory_default
        )

        # Inamic și NPC inițial de test
        goblin_class = DNDClass(name="Monster", primary_stat="DEX", health=15)
        goblin = Entity(dnd_class=goblin_class, name="Goblin", stats={"STR": 8}, position=(4, 2), location=self.current_location_name)
        self.global_enemies.append(goblin)

        npc_class = DNDClass(name="Civilian", primary_stat="CHA", health=5)
        mayor = Entity(dnd_class=npc_class, name="Mayor", stats={"CHA": 12}, position=(2, 3), location=self.current_location_name)
        self.global_npcs.append(mayor)

        self.load_local_entities()

    def add_story(self, text: str):
        self.story_log.append(text)

    def tick(self):
        self.game_time_seconds += 1
        self.map_class.mapData(self.local_enemies, self.local_npcs, self.player)
    
    def load_local_entities(self):
        self.local_enemies = {
            e.name.lower(): e for e in self.global_enemies 
            if getattr(e, 'location', '') == self.current_location_name
        }
        self.local_npcs = {
            n.name.lower(): n for n in self.global_npcs 
            if getattr(n, 'location', '') == self.current_location_name
        }

    def process_action(self, intent: dict,ai_dm=None) -> str:
        action = intent.get("action")
        target_name = intent.get("target")

        action_map = {
            "attack": lambda: self.action_attack(target_name),
            "talk": lambda: self.action_talk(target_name,ai_dm),
            "travel": lambda: self.action_travel(target_name,ai_dm),
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
            
        free_tile = self.map_class.getAdjacentFreeTile(tx, ty,self.local_enemies)
        if free_tile:
            self.player.position = free_tile
            self.needs_map_update = True
            return True, f"Player moved next to {target.name}. "
        else:
            return False, f"Cannot reach {target.name} because all adjacent spaces are blocked."

    def action_attack(self, target_name: str) -> str:
        if not target_name:
            return "Player attempted to attack but specified no valid target."
        
        target = self.local_enemies.get(target_name.lower())
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

    def action_talk(self, target_name: str, ai_dm=None) -> str:
        if not target_name:
            return "Player said something to the open air."
            
        target = self.local_npcs.get(target_name.lower()) or self.local_enemies.get(target_name.lower())
        
        if not target:
            return f"Player tried to talk to {target_name}, but they aren't here."
            
        reached_target, move_narrative = self.auto_approach(target)
        if not reached_target:
            return f"Talk failed. {move_narrative}"
                
        return move_narrative + f"Player said something to {target.name}. The NPC listened."
    
    def action_travel(self, target_name: str, ai_dm=None) -> str:
        if not target_name:
            return "Player tried to travel, but didn't specify where."
            
        target_key = target_name.lower()

        if target_key in self.visited_locations:
            self.add_story(f"*(Traveling back to {target_name}...)*")
            
            loc_data = self.visited_locations[target_key]
            self.current_location_name = loc_data["name"]
            
            self.map_class = MapClass(matrix=loc_data["matrix"])
            self.player.location = self.current_location_name
            self.player.position = (1, 1)
            
            self.load_local_entities() 
            self.needs_map_update = True
            return f"Player returned to {self.current_location_name}."

        else:
            if not ai_dm:
                return "Cannot travel. AI is not linked."

            self.add_story(f"*(Exploring new location: {target_name}...)*")
            
            new_world = ai_dm.generate_location(target_name)
            self.current_location_name = new_world.get("name", target_name)
            
            ai_matrix = new_world.get("matrix")
            if not ai_matrix:
                ai_matrix = [["1" if i==0 or i==9 or j==0 or j==9 else "0" for j in range(10)] for i in range(10)]

            self.visited_locations[self.current_location_name.lower()] = {
                "name": self.current_location_name,
                "matrix": ai_matrix
            }
            
            self.map_class = MapClass(matrix=ai_matrix)
            self.player.location = self.current_location_name
            self.player.position = (1, 1)

            h, w = self.map_class.size
            for i, edata in enumerate(new_world.get("enemies", [])):
                e_class = DNDClass(name="Monster", primary_stat="STR", health=edata.get("health", 15))
                en = Entity(dnd_class=e_class, name=f"{edata.get('name', 'Monster')} {i+1}", stats={"STR": 10}, position=(w-2, h-2), location=self.current_location_name)
                self.global_enemies.append(en)

            for i, ndata in enumerate(new_world.get("npcs", [])):
                n_class = DNDClass(name="Civilian", primary_stat="CHA", health=5)
                npc = Entity(dnd_class=n_class, name=ndata.get('name', f"Villager {i+1}"), stats={"CHA": 10}, position=(2, 2), location=self.current_location_name)
                self.global_npcs.append(npc)

            self.load_local_entities()
            self.needs_map_update = True
            return f"Player discovered {self.current_location_name}. {new_world.get('description', '')}"