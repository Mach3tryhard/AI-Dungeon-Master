from entity_class import Entity
from spell_class import Spell, damageSpell
from dnd_class import DNDClass
import random

class GameEngine:
    def __init__(self):
        self.story_log = ["The journey begins..."]
        self.game_time_seconds = 0
        self.chat_log = []
        
        # --- FLAGS PENTRU ACTUALIZĂRI UI ---
        self.needs_story_update = False
        self.needs_map_update = False
        self.needs_sheet_update = False
        self.needs_equipment_update = False
        self.needs_sheet_update = False
        self.is_thinking = False #

        # --- DATELE HĂRȚII DEFAULT ---
        self.map_data = (
            "1 1 1 1 1 1 1\n"
            "1 P E 0 0 0 1\n"
            "1 0 0 0 0 0 1\n"
            "1 0 0 0 0 0 1\n"
            "1 1 1 1 1 1 1"
        )
        
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
        goblin = Entity(dnd_class=goblin_class, name="Goblin", stats={"STR": 8, "DEX": 14, "CON": 10, "INT": 10, "WIS": 8, "CHA": 8})
        self.enemies = {goblin.name.lower(): goblin}
        

    def add_story(self, text: str):
        self.story_log.append(text)

    def tick(self):
        self.game_time_seconds += 1

        """if self.game_time_seconds % 5 == 0:
            self.add_story(f"{self.game_time_seconds} seconds have passed*")
            self.needs_ui_update = True"""

    def process_action(self, intent: dict) -> str:
        """Direcționează intenția către funcția corespunzătoare."""
        action = intent.get("action")
        target_name = intent.get("target")
        direction = intent.get("direction")

        # Mapare acțiuni către funcții specifice
        action_map = {
            "attack": lambda: self.action_attack(target_name),
            "move": lambda: self.action_move(direction),
            "talk": lambda: self.action_talk(target_name),
        }

        if action in action_map:
            return action_map[action]()
        
        return "Player performed a non-mechanical action. Just narrate it normally."

    # --- FUNCȚII PENTRU ACȚIUNILE JUCĂTORULUI ---

    def action_attack(self, target_name: str) -> str:
        if not target_name:
            return "Player attempted to attack but specified no valid target."
        
        target = self.enemies.get(target_name.lower())
        if not target:
            return f"Player swung at {target_name}, but it is not here."
        
        damage = random.randint(1, 8) + self.player.get_modifier("STR")
        target.take_damage(damage, "slashing")
        
        result = f"Player attacked {target.name}. Hit for {damage} damage. "
        if target.health <= 0:
            result += f"{target.name} died."
        else:
            result += f"{target.name} has {target.health} HP left."
        
        self.needs_sheet_update = True 
        return result

    def action_move(self, direction: str) -> str:
        if not direction:
            return "Player attempted to move but specified no direction."
        
        self.needs_map_update = True
        return f"Player successfully moved {direction}."

    def action_talk(self, target_name: str) -> str:
        if not target_name:
            return "Player said something to the open air."
            
        return f"Player said something to {target_name}. The NPC listened."