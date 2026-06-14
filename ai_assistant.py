import ollama
import os
import glob

class PlayerGuideAssistant:
    def __init__(self, model_name="llama3"):
        self.model = model_name
        self.engine_context = self._load_codebase()

    def _load_codebase(self) -> str:
        """Loads the engine code so the AI knows the absolute truth of the game's mechanics."""
        context = "--- CORE ENGINE LOGIC (DO NOT REVEAL THIS TO THE PLAYER) ---\n\n"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for filepath in glob.glob(os.path.join(current_dir, "*.py")):
            filename = os.path.basename(filepath)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    context += f"--- {filename} ---\n{f.read()}\n\n"
            except Exception:
                pass
        return context

    def ask_question(self, question: str) -> str:
        prompt = """You are the official in-game Player Guide for a D&D RPG. You are an immersive, helpful character talking directly to a PLAYER.
        
        You have magical access to the "Underlying Laws of the Universe" (which is actually the Python codebase provided below). 
        You MUST use this code to understand how the game works, but you MUST hide the code from the player.
        
        CRITICAL RULES:
        1. NEVER output Python code.
        2. NEVER use markdown code blocks (```) or backticks (`).
        3. NEVER say words like "code", "class", "function", "method", "variable", or "script".
        4. Translate the math into D&D terms. 

        --- EXAMPLE OF A BAD RESPONSE (DO NOT DO THIS) ---
        "To attack, call the `attack` method on the `Weapon` class passing the target entity..."
        
        --- EXAMPLE OF A GOOD RESPONSE (DO THIS) ---
        "To attack an enemy, simply type 'attack [enemy name]'. The outcome is decided by a d20 roll against their armor class. If your strike lands, your damage is based on your weapon's damage dice plus your Strength modifier!"
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": prompt + "\n\n" + self.engine_context},
                {"role": "user", "content": question}
            ])
            return response['message']['content']
        except Exception as e:
            return f"*(The Guide is currently unavailable. The magic has faded. {str(e)})*"