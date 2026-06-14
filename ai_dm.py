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

    def generate_dialogue(self, npc_name: str, npc_class: str, location_name: str, player_text: str, quest_state: str) -> str:
        prompt = f"""Ești {npc_name}, un {npc_class} care se află în {location_name}. 
        STAREA QUEST-ULUI: {quest_state}
        
        Răspunde direct jucătorului păstrând caracterul (in character). NU folosi format JSON, NU scrie text de sistem și nu adăuga acțiuni în afara ghilimelelor. Generează doar ceea ce spui verbal și scurte acțiuni fizice (ex: *îți dă o pungă de bani*)."""
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Jucătorul zice: {player_text}"}
            ])
            return response['message']['content']
        except Exception:
            return f"{npc_name} se uită la tine în tăcere. (Eroare de Sistem)"

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
