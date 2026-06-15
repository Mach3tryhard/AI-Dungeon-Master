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
            "action": "attack" | "travel" | "talk" | "look" | "other",
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

    def generate_dialogue(self, npc_name: str, npc_class: str, location_name: str, player_text: str, quest_state: str, luck_roll: int) -> str:
        prompt = f"""You are {npc_name}, a {npc_class} currently located in {location_name}. 
        QUEST STATE: {quest_state}
        PLAYER'S D20 ROLL (1-20): {luck_roll}. (A low roll means you are reluctant, grumpy, or distrustful. A high roll means you are extremely friendly and helpful).
        
        Respond directly to the player IN CHARACTER. DO NOT use JSON format, DO NOT write system text, and DO NOT add actions outside of asterisks. Generate ONLY your spoken dialogue and short physical actions (e.g., *hands you a pouch of coins*). SPEAK STRICTLY IN ENGLISH."""
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"The player says: {player_text}"}
            ])
            return response['message']['content']
        except Exception:
            return f"{npc_name} stares at you in silence. (System Error)"

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
