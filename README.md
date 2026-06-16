# AI Dungeon Master: Terminal RPG

A highly immersive, text-based Dungeons & Dragons experience built entirely in Python. This project bridges the gap between traditional deterministic game engines and modern Generative AI, featuring a fully functional Terminal User Interface (TUI) and an AI Dungeon Master that dynamically narrates your actions, controls NPCs, and acts as a code-aware player guide.

## Core Features

* **Deterministic Game Engine:** Under the hood, a strict Python engine handles stats, HP tracking, inventory, map coordinates, and d20 dice rolls to ensure fair and mathematically sound gameplay.
* **AI-Powered Narrative:** The engine's raw numerical outputs (e.g., "Player rolled 18, dealt 6 damage, Goblin has 4 HP left") are fed directly into a local Large Language Model (Llama 3) to generate rich, contextual, and immersive storytelling on the fly.
* **Dynamic Turn-Based Combat:** Engage in combat with automated enemy counter-attacks, weapon damage calculation, and a seamless Game Over/Restart loop.
* **Intelligent NPC Dialogue:** Talk to characters in the world. The AI generates their responses based on the current game state, remaining enemies, and active quests.
* **Code-Aware Player Guide:** An in-game assistant that can read the project's actual `.py` source code to accurately teach players how to use the game's mechanics without hallucinating controls.
* **Modern TUI:** A responsive terminal interface built with Textual, featuring pop-up modals, stat tracking, and real-time chat logs.
* **Automated CI/CD Pipeline:** Fully integrated GitHub Actions workflow for testing (`pytest`) and automatically compiling portable `.exe` releases using PyInstaller.

## Tech Stack

* **Language:** Python 3.12+
* **Interface:** [Textual](https://textual.textualize.io/) (for the TUI)
* **AI Engine:** [Ollama](https://ollama.com/) (running Llama 3 locally)
* **Testing & Build:** `pytest`, GitHub Actions, PyInstaller

## How to Play (Portable Release)

The easiest way to play the game is by downloading the latest automated release. No Python installation is required!

1. Go to the **Releases** tab on this GitHub repository.
2. Download the latest `DND_Game.zip` archive.
3. Extract the folder to your Desktop or Documents (Do not run it directly from inside the ZIP).
4. Ensure you have [Ollama](https://ollama.com/) installed and running on your system with the `llama3` model pulled (`ollama run llama3`).
5. Double-click `tui.exe` to start the adventure!

## Developer Setup (Running from Source)

If you want to modify the codebase or run the game directly through Python:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Dungeon-Master.git
cd AI-Dungeon-Master
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Ollama server in the background (if not already running).
4. Launch the game interface:
```bash
python UI/tui.py
```

## Project Architecture

* `UI/tui.py`: The main entry point. Handles the Textual application, layout, styling, and user input mapping.
* `engine.py`: The core deterministic logic. Manages combat math, movement, state tracking, and the underlying rules of the universe.
* `ai_dm.py`: The translation layer between the game engine and the Ollama API. Injects engine data into system prompts to generate the narrative.
* `presets.py`: Data dictionaries containing class stats, starting equipment, and race bonuses.
* `.github/workflows/`: Contains the CI/CD configuration for automated smoke testing and executable generation.

## 👨‍💻 Authors

**Matei Sîrghe-Ștefan** 
**Ștefan Bujor** 
*Computer Science Engineering Students* 
University of Bucharest, Faculty of Mathematics and Informatics

<img width="1887" height="981" alt="image" src="https://github.com/user-attachments/assets/87774ba6-c084-492e-af4f-20cd2b354ddf" />
<img width="1887" height="975" alt="image" src="https://github.com/user-attachments/assets/75ab020b-315c-474f-9410-84954ccdf128" />
<img width="1879" height="954" alt="image" src="https://github.com/user-attachments/assets/ea81eb0b-afe4-45a6-9a1b-e4714dfeb773" />
<img width="1884" height="949" alt="image" src="https://github.com/user-attachments/assets/a02a08a8-5a02-4a04-93a7-58112e627d10" />
<img width="1879" height="952" alt="image" src="https://github.com/user-attachments/assets/1982b457-76cf-416f-b919-799d3f8c1233" />
