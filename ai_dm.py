import ollama
import json
import subprocess
import time

class AIDungeonMaster:
    def __init__(self, model_name="llama3"):
        self.model = model_name

    def parse_intent(self, player_text: str) -> dict:
        prompt = """You are a game engine parser. Extract the user's intent into strict JSON.
        Schema:
        {
            "action": "attack" | "travel" | "talk" | "cast_spell" | "other",
            "target": "name of entity" or null,
            "direction": "north" | "south" | "east" | "west" or null
        }
        """
        try:
            response = ollama.chat(model=self.model, format='json', messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": player_text}
            ])
            return json.loads(response['message']['content'])
        except Exception:
            return {"action": "error", "target": None, "direction": None}

    def generate_location(self, location_name: str) -> dict:
        prompt = """You are a D&D World Builder. The player is traveling to a new location.
                    Generate the location details in strict JSON format. 
                    IMPORTANT: Include a "matrix" which is a 2D array representing the map using "0" for empty, "1" for walls, and "2" for obstacles. Keep maps between 10x10 and 20x20.
                    Schema:
                    {
                        "name": "Name of the place",
                        "description": "Short visual description",
                        "matrix": [
                            ["1", "1", "1", "1"],
                            ["1", "0", "0", "1"],
                            ["1", "1", "1", "1"]
                        ],
                        "enemies": [
                            {"name": "Goblin", "health": 15, "str": 8, "dex": 14}
                        ],
                        "quests": [
                            {"title": "Clear the camp", "description": "Kill all enemies.", "giver": "NPC Name"}
                        ]
                    }"""
        try:
            response = ollama.chat(model=self.model, format='json', messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Generate location: {location_name}"}
            ])
            return json.loads(response['message']['content'])
        except Exception:
            return {
                "name": location_name,
                "description": "A mysterious empty place.",
                "matrix": [["1","1","1"],["1","0","1"],["1","1","1"]],
                "enemies": [],
                "quests": []
            }

    def generate_npc_quest(self, npc_name: str, location: str) -> dict:
        prompt = f"""You are a D&D Quest Generator. The player talks to {npc_name} in {location}. Generate a simple kill quest.
        Schema:
        {{
            "title": "Quest Title",
            "description": "Short quote from the NPC asking for help.",
            "giver": "{npc_name}",
            "target_enemy": "Name of a specific monster type",
            "target_count": 1
        }}"""
        try:
            response = ollama.chat(model=self.model, format='json', messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Generate quest for {npc_name}"}
            ])
            return json.loads(response['message']['content'])
        except Exception:
            return {
                "title": f"Help {npc_name}",
                "description": "Please defeat the monster nearby.",
                "giver": npc_name,
                "target_enemy": "Monster",
                "target_count": 1
            }

    def narrate_outcome(self, player_text: str, engine_result: str) -> str:
        prompt = """You are a D&D Dungeon Master. Narrate the outcome of the player's action in 2-3 sentences based exactly on the engine's result. Add descriptive flavor but do not invent mechanics or change the facts."""
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Player Action: {player_text}\nEngine Result: {engine_result}"}
            ])
            return response['message']['content']
        except Exception:
            return f"*(System Error: Failed to narrate. Raw result: {engine_result})*"
