import sys
import os
import traceback

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def run_complex_smoke_test():
    print("Starting Smoke Test")
    try:
        print("1. Testing imports...")
        from UI.tui import DNDGameApp
        from engine import GameEngine
        from presets import CLASS_STATS, RACE_BONUSES, STARTING_EQUIPMENT
        
        print("2. Verifying game data dictionaries...")
        assert "Wizard" in CLASS_STATS, "Wizard class is missing from presets!"
        assert "gold" in STARTING_EQUIPMENT["Rogue"], "Rogue has no starting gold defined!"
        
        print("3. Booting up GameEngine...")
        engine = GameEngine()
        assert engine.player is not None, "Player entity failed to initialize!"
        
        print("4. Simulating character stat injection...")
        engine.player.name = "TestHero"
        engine.player.dnd_class.name = "Fighter"
        engine.player.stats = CLASS_STATS["Fighter"].copy()
        engine.player.health = CLASS_STATS["Fighter"]["HP"]
        
        assert engine.player.health == 12, "Player HP did not map correctly from presets!"

        print("SMOKE TEST PASSED!")
        sys.exit(0)
        
    except Exception as e:
        print("\nSMOKE TEST FAILED:\n")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_complex_smoke_test()