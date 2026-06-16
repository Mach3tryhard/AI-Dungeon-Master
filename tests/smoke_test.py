import sys
import traceback
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def run_smoke_test():
    print("--Smoke Test--")
    try:
        
        print("--Testare importuri--")
        from UI.tui import DNDGameApp
        from engine import GameEngine
        from presets import CLASS_STATS, RACE_BONUSES
        
        print("--Testare integritate presets--")
        assert "Fighter" in CLASS_STATS, "Clasa Fighter lipsește!"
        assert "Human" in RACE_BONUSES, "Rasa Human lipsește!"
        
        print("Instanțiere GameEngine...")
        engine = GameEngine()
        assert engine.player is not None, "Jucătorul nu a fost creat în engine!"
        
        print("SMOKE TEST TRECUT CU SUCCES!")
        
    except Exception as e:
        print("\nSMOKE TEST EȘUAT:\n")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_smoke_test()