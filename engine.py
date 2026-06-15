from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
from map_class import MapClass
from utils import Dice
from weapon_class import Weapon
from inventory_class import Inventory
from database.db_manager import *
from database.init_db import *
from database.db_manager import DatabaseManager
import json 

import random

class GameEngine:
    def __init__(self):
        self.story_log = ["The journey begins..."]
        self.game_time_seconds = 0
        self.chat_log = []
        self.in_combat = False

        self.db = DatabaseManager("dnd_database.db")

        self.personalities = ["sarcastic", "mean", "preppy", "clumsy", "sleepy", "scared", "brave", "lazy", "smart"]
        self.jobs = ["bartender", "knight", "blacksmith", "ranger", "wizard", "chef", 
                     "royalty", "king", "paladin", "priest", "hero", "painter",
                     "historian"]
        self.map_class = MapClass((20,20))
        self.current_location_name = "forest"
        
        self.visited_locations = {} 
        self.visited_locations[self.current_location_name] = {
            "name": self.current_location_name,
            "matrix": self.map_class.base_map,
            # "enmies": self.local_enemies
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

        init_database()
        
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

    def db_fetch_location_data(self, location_name: str) -> dict:
        
        map_db = self.db.get_map()
        if map_db and map_db.get("layout"):
            try:
                matrix = json.loads(map_db["layout"]) 
            except Exception:
                matrix = [["1" if i==0 or i==9 or j==0 or j==9 else "0" for j in range(10)] for i in range(10)]
        else:
            matrix = [["1" if i==0 or i==9 or j==0 or j==9 else "0" for j in range(10)] for i in range(10)]

        enemy_positions = []
        npc_positions = []
        player_position = (1, 1) 
        
        base_matrix = []
        for y, row in enumerate(matrix):
            base_row = []
            for x, cell in enumerate(row):
                if cell == 'E':
                    enemy_positions.append((x, y))
                    base_row.append('0')
                elif cell == 'N':
                    npc_positions.append((x, y))
                    base_row.append('0')
                elif cell == 'P':
                    player_position = (x, y)
                    base_row.append('0')
                else:
                    base_row.append(cell)
            base_matrix.append(base_row)

        enemies_data = []
        for _ in range(len(enemy_positions)):
            e_data = self.db.get_random_enemy()
            if e_data:
                enemies_data.append(e_data)

        npcs_data = []
        for _ in range(len(npc_positions)):
            n_data = self.db.get_random_npc()
            if n_data:
                npcs_data.append(n_data)

        return {
            "name": location_name,
            "matrix": base_matrix,
            "enemy_positions": enemy_positions,
            "npc_positions": npc_positions,
            "player_position": player_position,
            "enemies": enemies_data,
            "npcs": npcs_data
        }

    # --- FUNCȚII PENTRU ACȚIUNILE JUCĂTORULUI ---

    def process_action(self, intent: dict, player_text: str = "", ai_dm=None) -> tuple[int, str]:
        action = intent.get("action")
        target_name = intent.get("target")

        luck_roll = random.randint(1, 20)

        action_map = {
            "attack": lambda: self.action_attack(target_name, luck_roll),
            "talk": lambda: self.action_talk(target_name, player_text, luck_roll, ai_dm),
            "travel": lambda: self.action_travel(target_name, luck_roll),
            "look": lambda: self.action_look(luck_roll),
        }

        if action in action_map:
            return luck_roll, action_map[action]()
        
        return luck_roll, "Player performed a non-mechanical action. Just narrate it normally."

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

    def action_attack(self, target_name: str, luck_roll: int) -> str:
        if not target_name:
            return "Attack failed: No valid target specified."
        
        target = self.local_enemies.get(target_name.lower())
        if not target:
            return f"Attack failed: {target_name} is not here."
            
        if target.health <= 0:
            return f"Attack failed: {target.name} is already dead."

        reached_target, move_narrative = self.auto_approach(target)
        if not reached_target:
            return f"Attack failed. {move_narrative}"
        
        if self.player.inventory and self.player.inventory.items:
            weapon = self.player.inventory.items[0]
            try:
                count, sides = map(int, weapon.damage_roll.split('d'))
                weapon_dmg = sum(random.randint(1, sides) for _ in range(count))
                dmg_type = weapon.damage_type
                weapon_name = weapon.name
            except Exception:
                weapon_dmg = random.randint(1, 4)
                dmg_type = "bludgeoning"
                weapon_name = "fists"
        else:
            weapon_dmg = random.randint(1, 4)
            dmg_type = "bludgeoning"
            weapon_name = "fists"
        
        bonus_din_zar = luck_roll // 10
        damage = weapon_dmg + bonus_din_zar + self.player.get_modifier("STR")
        
        if damage < 1: 
            damage = 1
            
        target.take_damage(damage, dmg_type)
        
        result = move_narrative + f"Player rolled a {luck_roll} and HIT {target.name} using {weapon_name} for {damage} {dmg_type} damage. "
        
        if target.health <= 0:
            result += f"{target.name} died."
        else:
            result += f"{target.name} has {target.health} HP left."
        
        self.needs_sheet_update = True 
        self.needs_map_update = True
        return result

    def action_talk(self, target_name: str, player_text: str, luck_roll: int, ai_dm=None) -> str:
        if not target_name: return "Player said something to the open air."
            
        target = self.local_npcs.get(target_name.lower())
        if not target:
            enemy_target = self.local_enemies.get(target_name.lower())
            if enemy_target:
                return f"{enemy_target.name} is hostile and doesn't want to talk!"
            return f"Player tried to talk to {target_name}, but they aren't here."
            
        reached_target, move_narrative = self.auto_approach(target)
        if not reached_target: return f"Talk failed. {move_narrative}"
                
        alive_enemies = [e for e in self.local_enemies.values() if getattr(e, 'health', 0) > 0]
        enemies_count = len(alive_enemies)
        npc_class = getattr(target.dnd_class, 'name', 'villager') if hasattr(target, 'dnd_class') else "villager"

        # TRANSLATED TO ENGLISH
        if enemies_count > 0:
            enemy_names = list(set([e.name for e in alive_enemies]))
            enemies_list_str = ", ".join(enemy_names)
            quest_context = f"There are {enemies_count} enemies remaining in the area (Detected creatures: {enemies_list_str}). Beg the player to help you and specifically mention the creatures you are afraid of. Promise them a reward."
        else:
            if not getattr(target, 'quest_completed', False):
                reward = 100
                self.player.inventory.add_gold(reward)
                self.needs_equipment_update = True
                target.quest_completed = True
                quest_context = f"The map is cleared! The player killed all the enemies. Thank them profusely and offer them {reward} Gold coins as a reward."
            else:
                quest_context = "The enemies are dead, and you already gave the player their reward. Now just thank them again for saving the region."

        if ai_dm:
            dialogue = ai_dm.generate_dialogue(
                npc_name=target.name,
                npc_class=npc_class,
                location_name=self.current_location_name,
                player_text=player_text,
                quest_state=quest_context,
                luck_roll=luck_roll
            )
            return f"{move_narrative}[bold cyan][Charisma/Luck Roll: {luck_roll}][/] {dialogue}"
        else:
            return move_narrative + f"Player talked to {target.name}."

    def action_look(self, luck_roll: int) -> str:
        alive_enemies = [e.name for e in self.local_enemies.values() if getattr(e, 'health', 0) > 0]
        npcs = [n.name for n in self.local_npcs.values()]
        
        result = f"[bold cyan][Perception Roll: {luck_roll}][/] Scanning '{self.current_location_name}': "
        
        if luck_roll < 5:
            return result + "You glance around, but your vision is blurry or you are distracted. It's hard to make out details."
            
        if alive_enemies:
            result += f"Hostile threats detected -> {', '.join(alive_enemies)}. "
        else:
            result += "No hostile threats detected. "
            
        if npcs:
            result += f"NPCs present -> {', '.join(npcs)}."
        else:
            result += "No friendly faces around."
            
        return result
    
    def action_travel(self, target_name: str, luck_roll: int) -> str:
        if not target_name: return "Travel failed: No destination."
            
        target_key = target_name.lower()

        if target_key in self.visited_locations:
            loc_data = self.visited_locations[target_key]
            self.current_location_name = loc_data["name"]
            self.map_class = MapClass(matrix=loc_data["matrix"])
            self.player.position = loc_data.get("player_position", (1, 1))
        else:
            db_data = self.db_fetch_location_data(target_name)
            self.current_location_name = db_data["name"]
            ai_matrix = db_data["matrix"]
            p_pos = db_data["player_position"]

            self.visited_locations[self.current_location_name.lower()] = {
                "name": self.current_location_name,
                "matrix": ai_matrix,
                "player_position": p_pos
            }
            self.map_class = MapClass(matrix=ai_matrix)

            for i, edata in enumerate(db_data.get("enemies", [])):
                e_class_db = self.db.get_dnd_class(edata["dnd_class"])
                hp = e_class_db["health"] if e_class_db else 15
                e_class = DNDClass(name=edata["dnd_class"], primary_stat="STR", health=hp)
                
                pos = db_data["enemy_positions"][i]
                en = Entity(dnd_class=e_class, name=edata["name"], stats={"STR": 10, "DEX": 10}, 
                            position=pos, location=self.current_location_name)
                self.global_enemies.append(en)

            for i, ndata in enumerate(db_data.get("npcs", [])):
                n_class_db = self.db.get_dnd_class(ndata["dnd_class"])
                hp = n_class_db["health"] if n_class_db else 10
                n_class = DNDClass(name=ndata["dnd_class"], primary_stat="CHA", health=hp)
                
                pos = db_data["npc_positions"][i]
                npc = Entity(dnd_class=n_class, name=ndata["name"], stats={"CHA": 12, "DEX": 10}, 
                             position=pos, location=self.current_location_name)
                self.global_npcs.append(npc)
                
            self.player.position = p_pos

        self.player.location = self.current_location_name
        self.load_local_entities() 
        self.needs_map_update = True
        
        return f"Player rolled a {luck_roll} for travel luck. Entered {self.current_location_name}."