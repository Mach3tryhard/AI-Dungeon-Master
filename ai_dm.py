import ollama
import json

class AIDungeonMaster:
    def __init__(self, model_name="llama3"):
        self.model = model_name

    def parse_intent(self, player_text: str) -> dict:
        """PASS 1: Forces the AI to extract intent into a strict JSON format."""
        prompt = """You are a game engine parser. Extract the user's intent into strict JSON.
        Schema:
        {
            "action": "attack" | "move" | "talk" | "cast_spell" | "other",
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