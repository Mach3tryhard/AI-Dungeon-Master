import sys
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, ScrollableContainer, Vertical, Horizontal, Middle,Center
from textual.widgets import Header, Footer, Static, Input, Label, Button, Select
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
import random
from engine import GameEngine
from ai_dm import AIDungeonMaster
import presets

from UI.map_screen import MapScreen
from UI.sheet import CharacterSheetScreen
from UI.assistant_screen import AssistantScreen

class GameOverScreen(ModalScreen[str]):

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                with Vertical(id="game-over-dialog"):
                    yield Label("💀 YOU DIED 💀", id="game-over-title")
                    yield Label("Your adventure had ended.", id="game-over-text")
                    
                    with Center():
                        yield Button("Restart Game", id="btn-restart", variant="error")
                        yield Button("Quit to Desktop", id="btn-quit", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-restart":
            self.dismiss("restart")
        elif event.button.id == "btn-quit":
            self.dismiss("quit")

class AttackModal(ModalScreen[bool]):
    CSS = "AttackModal { align: center middle; background: $background 50%; } #attack-dialog { width: 45; height: auto; padding: 1; border: thick $error; background: $surface; } .attack-title { text-style: bold; color: $error; margin-bottom: 1; } .dialog-buttons { height: auto; align: center middle; } .modal-btn { margin: 1; }"
    
    def __init__(self, target: str, **kwargs):
        self.target = target or "Unknown Target"
        super().__init__(**kwargs)
        
    def compose(self):
        with Vertical(id="attack-dialog"):
            yield Label("⚔️ INITIATE ATTACK", classes="attack-title")
            yield Label(f"Draw your weapon and attack {self.target}?")
            yield Label("[dim]Rolls a d20 to calculate attack damage.[/dim]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Strike", variant="error", id="btn-confirm", classes="modal-btn")
                yield Button("Cancel", variant="primary", id="btn-cancel", classes="modal-btn")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")


class TalkModal(ModalScreen[bool]):
    CSS = "TalkModal { align: center middle; background: $background 50%; } #talk-dialog { width: 45; height: auto; padding: 1; border: thick $accent; background: $surface; } .talk-title { text-style: bold; color: $accent; margin-bottom: 1; } .dialog-buttons { height: auto; align: center middle; } .modal-btn { margin: 1; }"
    
    def __init__(self, target: str, **kwargs):
        self.target = target or "Anyone Nearby"
        super().__init__(**kwargs)
        
    def compose(self):
        with Vertical(id="talk-dialog"):
            yield Label("🗣️ INITIATE DIALOGUE", classes="talk-title")
            yield Label(f"Approach and speak to {self.target}?")
            yield Label("[dim]Rolls a d20 to determine NPC disposition.[/dim]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Speak", variant="primary", id="btn-confirm", classes="modal-btn")
                yield Button("Cancel", variant="error", id="btn-cancel", classes="modal-btn")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")


class TravelModal(ModalScreen[bool]):
    CSS = "TravelModal { align: center middle; background: $background 50%; } #travel-dialog { width: 45; height: auto; padding: 1; border: thick $success; background: $surface; } .travel-title { text-style: bold; color: $success; margin-bottom: 1; } .dialog-buttons { height: auto; align: center middle; } .modal-btn { margin: 1; }"
    
    def __init__(self, destination: str, **kwargs):
        self.destination = destination or "Unknown Lands"
        super().__init__(**kwargs)
        
    def compose(self):
        with Vertical(id="travel-dialog"):
            yield Label("🧭 TRAVEL CONFIRMATION", classes="travel-title")
            yield Label(f"Pack your gear and travel to {self.destination}?")
            yield Label("[dim]Rolls a d20 to determine travel luck.[/dim]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Travel", variant="success", id="btn-confirm", classes="modal-btn")
                yield Button("Stay Here", variant="error", id="btn-cancel", classes="modal-btn")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")


class LookModal(ModalScreen[bool]):
    CSS = "LookModal { align: center middle; background: $background 50%; } #look-dialog { width: 45; height: auto; padding: 1; border: thick $warning; background: $surface; } .look-title { text-style: bold; color: $warning; margin-bottom: 1; } .dialog-buttons { height: auto; align: center middle; } .modal-btn { margin: 1; }"
    
    def compose(self):
        with Vertical(id="look-dialog"):
            yield Label("👁️ PERCEPTION CHECK", classes="look-title")
            yield Label("Scan your surroundings?")
            yield Label("[dim]Rolls a d20 to determine what you notice.[/dim]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Look", variant="warning", id="btn-confirm", classes="modal-btn")
                yield Button("Cancel", variant="error", id="btn-cancel", classes="modal-btn")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")

class SleepModal(ModalScreen[bool]):
    CSS = "SleepModal { align: center middle; background: $background 50%; } #look-dialog { width: 45; height: auto; padding: 1; border: thick $warning; background: $surface; } .look-title { text-style: bold; color: $warning; margin-bottom: 1; } .dialog-buttons { height: auto; align: center middle; } .modal-btn { margin: 1; }"
    
    def compose(self):
        with Vertical(id="look-dialog"):
            yield Label("🛏️ SLEEP CHECK", classes="look-title")
            yield Label("Choose to fall asleep?")
            yield Label("[dim]Rolls a d20 to determine how you sleep.[/dim]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Look", variant="warning", id="btn-confirm", classes="modal-btn")
                yield Button("Cancel", variant="error", id="btn-cancel", classes="modal-btn")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")

ASCII_WIZARD = """
          /\ 
         /  \ 
        /____\ 
       ( '  ' )
       _) -- (_
      /  >__<  \    *
     / /|    |\ \   |
    / / |    | \ \  |
   ( /  |    |  \ \ |
    \   |____|   \_\|
        |    |      |
        |____|      |
        /    \      |
       (______)    _|_
"""
dice = ["d4", "d6", "d8", "d10", "d12", "d20"]

D20_FRAMES = [
    "   ____   \n"
    "  /\\  /\\  \n"
    " /  \\/  \\ \n"
    " \\  {val}  / \n"
    "  \\    /  \n"
    "   \\__/   ",
    
    "   ____   \n"
    "  /____\\  \n"
    " / \\  / \\ \n"
    " \\  {val}  / \n"
    "  \\ \\/ /  \n"
    "   \\__/   ",
    
    "   ____   \n"
    "  /|  |\\  \n"
    " / |__| \\ \n"
    " \\  {val}  / \n"
    "  \\ |  /  \n"
    "   \\|/   "
]

class TumblingD20(Static):
    def __init__(self, final_value: int, **kwargs):
        super().__init__(**kwargs)
        self.final_value = final_value
        self.ticks = 0
        self.max_ticks = 20
        
        self.styles.width = "auto"
        self.styles.height = "auto"
        self.styles.text_align = "center"

    def on_mount(self) -> None:
        self.animation_timer = self.set_interval(0.1, self.animate_roll)

    def animate_roll(self) -> None:
        self.ticks += 1
        
        if self.ticks < self.max_ticks:
            frame_idx = self.ticks % len(D20_FRAMES)
            fake_val = random.randint(1, 20)
            val_str = f"{fake_val:>2}" 
            color = random.choice(["$accent", "$warning", "$error", "$success"])
            art = D20_FRAMES[frame_idx].format(val=val_str)
            self.update(f"[bold {color}]{art}[/]")
        else:
            val_str = f"{self.final_value:>2}"
            art = D20_FRAMES[0].format(val=val_str)
            color = "$success" if self.final_value >= 10 else "$error"
            self.update(f"[bold {color}]{art}[/]\n  [dim]Roll: {self.final_value}[/]")
            self.animation_timer.pause()

# --- App Logic ---

class DNDGameApp(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("ctrl+s", "show_sheet", "Open Character Sheet"),
        ("ctrl+o", "show_map", "Open Map"),
        ("ctrl+g", "show_guide", "Open Guide"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Grid(id="dnd-main"):
            with Container(id="left-column"):
                yield Static("DUNGEON MASTER", id="dm-title")  

                yield Static(ASCII_WIZARD, id="wizard-box")
                
                yield Static("D20 LUCK ROLL", id="stats-separator")
                dice_area = Container(id="dice-area")
                dice_area.styles.align = ("center", "middle")
                yield dice_area

            with ScrollableContainer(id="right-column"):
                yield Static("[bold] Story log [/]\n", id="chat-panel")
                yield Static("[bold] Equipment [/]", id="weapon-info-panel")
                yield Input(placeholder="Your action...", id="dm-input")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "AI DM: Dungeons & Dragons"
        
        self.push_screen(CharacterCreatorScreen(), self.on_character_created)

    def on_character_created(self, char_data: tuple) -> None:
        name, char_class, char_race, char_bg = char_data
        
        self.engine = GameEngine()
        self.ai_dm = AIDungeonMaster(model_name="llama3")
        
        base_stats = presets.CLASS_STATS.get(char_class, presets.CLASS_STATS["Fighter"]).copy()
        race_bonuses = presets.RACE_BONUSES.get(char_race, presets.RACE_BONUSES["Human"])
        
        for stat in base_stats:
            if stat != "HP":
                base_stats[stat] += race_bonuses.get(stat, 0)

        self.engine.player.name = name
        self.engine.player.dnd_class.name = char_class
        self.engine.player.stats = base_stats
        self.engine.player.health = base_stats["HP"]
        self.engine.player.max_health = base_stats["HP"]

        equipment = presets.STARTING_EQUIPMENT.get(char_class, presets.STARTING_EQUIPMENT["Fighter"])
        
        if hasattr(self.engine.player, "inventory"):
            self.engine.player.inventory.gold = equipment["gold"]
            
            class StartingWeapon:
                pass
            
            w_data = equipment["weapon"]
            weapon = StartingWeapon()
            weapon.name = w_data["name"]
            weapon.damage_roll = w_data["damage_roll"]
            weapon.damage_type = w_data["damage_type"]
            weapon.range = w_data["range"]
            weapon.level = w_data["level"]
            
            self.engine.player.inventory.items = [weapon]

        traits = presets.CLASS_TRAITS.get(char_class, [])
        self.engine.player.traits = traits
        
        intro_text = (
            f"Welcome to the realm, {name}. As a {char_race} {char_class} with a background as a {char_bg}, "
            f"you possess unique skills: {', '.join(traits)}. Your adventure begins now. What do you do?"
        )
        self.engine.chat_log.append(f"[bold $secondary]DM:[/] {intro_text}")
        
        self.update_story_display()
        self.update_equipment_display()
        self.set_interval(1.0, self.game_loop)

    def game_loop(self) -> None:
        self.engine.tick()

        if self.engine.needs_equipment_update:
            self.update_equipment_display()
            self.engine.needs_equipment_update = False

        if self.engine.needs_story_update:
            self.update_story_display()
            self.engine.needs_story_update = False

        if self.engine.needs_map_update:
            if isinstance(self.screen, MapScreen):
                self.screen.refresh_map()
            self.engine.needs_map_update = False

        if self.engine.needs_sheet_update:
            if isinstance(self.screen, CharacterSheetScreen):
                self.screen.refresh_sheet()
            self.engine.needs_sheet_update = False

    def update_story_display(self) -> None:
        chat_panel = self.query_one("#chat-panel", Static)
        chat_text = "\n".join(self.engine.chat_log)
        
        if getattr(self.engine, "is_thinking", False):
            chat_text += "\n\n[i yellow]*(The DM is rolling dice and thinking...)*[/]"
            
        chat_panel.update("[bold] Story Log [/]\n" + chat_text)

    def update_equipment_display(self) -> None:
        equip_panel = self.query_one("#weapon-info-panel", Static)

        if not hasattr(self.engine.player, "inventory") or not self.engine.player.inventory.items:
            equip_panel.update("## Equipment\n[dim italic]Inventory is empty.[/]")
            return

        item_blocks = []

        for item in self.engine.player.inventory.items:
            item_text = (
                f"- [cornflowerblue]{item.name}[/] [dim](Lvl {item.level})[/]\n"
                f"  Damage: [red]{item.damage_roll}[/] {item.damage_type}\n"
                f"  Range: {item.range}"
            )
            item_blocks.append(item_text)

        full_equip = '\n\n'.join(item_blocks)
        equip_panel.update(f"[bold] Equipment [/]\n{full_equip}")

    @on(Input.Submitted, "#dm-input")
    def handle_player_action(self, event: Input.Submitted) -> None:
        player_text = event.value
        if not player_text.strip(): return
        
        event.input.value = "" 
        self.engine.chat_log.append(f"[bold green]You:[/] {player_text}")
        self.engine.is_thinking = True
        self.update_story_display()
        
        intent = self.ai_dm.parse_intent(player_text)
        action = intent.get("action")
        target = intent.get("target")
        
        def on_modal_confirm(confirmed: bool):
            if confirmed:
                self.process_turn_background(intent, player_text)
            else:
                self.engine.chat_log.append("[bold red]Action Cancelled.[/]")
                self.engine.is_thinking = False
                self.update_story_display()

        if action == "attack":
            self.push_screen(AttackModal(target), on_modal_confirm)
        elif action == "talk":
            self.push_screen(TalkModal(target), on_modal_confirm)
        elif action == "travel":
            self.push_screen(TravelModal(target), on_modal_confirm)
        elif action == "look":
            self.push_screen(LookModal(), on_modal_confirm)
        elif action == "sleep":
            self.push_screen(SleepModal(), on_modal_confirm)
        else:
            on_modal_confirm(True)

    @work(thread=True)
    def process_turn_background(self, intent: dict, player_text: str) -> None:
        luck_roll, engine_result = self.engine.process_action(intent, player_text=player_text, ai_dm=self.ai_dm)
        
        self.app.call_from_thread(self.trigger_d20_animation, luck_roll)
        
        if intent.get("action") in ["talk", "look"]:
            narrative = engine_result
        else:
            narrative_text = self.ai_dm.narrate_outcome(player_text, engine_result)
            action_type = str(intent.get("action")).capitalize()
            narrative = f"[bold cyan][{action_type} D20 Roll: {luck_roll}][/] {narrative_text}"
        
        self.app.call_from_thread(self.finalize_turn, narrative)

    def finalize_turn(self, narrative: str) -> None:
        self.engine.is_thinking = False
        
        self.engine.chat_log.append(f"[bold $secondary]DM:[/] {narrative}")
        
        self.engine.add_story(narrative) 
        
        self.update_story_display()

        if getattr(self.engine, 'is_game_over', False) or self.engine.player.health <= 0:
            self.push_screen(GameOverScreen(), self.handle_game_over)

    def trigger_d20_animation(self, final_value: int) -> None:
        container = self.query_one("#dice-area")
        
        for child in container.children:
            child.remove()
            
        container.mount(TumblingD20(final_value=final_value, classes="die-center"))

    def action_show_sheet(self) -> None:
        if not isinstance(self.screen, CharacterSheetScreen):
            self.push_screen(CharacterSheetScreen())
    def action_show_map(self) -> None:
        if not isinstance(self.screen, MapScreen):
            self.push_screen(MapScreen())
    def action_show_guide(self) -> None:
        if not isinstance(self.screen, AssistantScreen):
            self.push_screen(AssistantScreen())

    def handle_game_over(self, choice: str) -> None:
        if choice == "quit":
            self.exit()
        elif choice == "restart":

            chat_panel = self.query_one("#chat-panel")
            chat_panel.update("A new soul enters the realm. What is your name?")

            self.push_screen(CharacterCreatorScreen(), self.on_character_created)

class CharacterCreatorScreen(Screen):
    CSS = """
    CharacterCreatorScreen {
        align: center middle;
        background: $background 80%;
    }
    #char-creator-container {
        width: 50;
        height: auto;
        padding: 2;
        border: thick $primary;
        background: $surface;
    }
    #char-creator-title {
        text-style: bold;
        color: $primary;
        margin-bottom: 2;
        content-align: center middle;
        width: 100%;
    }
    Input, Select {
        margin-bottom: 1;
    }
    #btn-start {
        width: 100%;
        margin-top: 1;
    }
    """

    def compose(self):
        with Vertical(id="char-creator-container"):
            yield Label("📜 CREATE YOUR CHARACTER", id="char-creator-title")
            
            yield Input(placeholder="Character Name", id="char-name")
            
            class_options = [(c, c) for c in presets.CLASS_STATS.keys()]
            race_options = [(r, r) for r in presets.RACE_BONUSES.keys()]
            bg_options = [(b, b) for b in presets.BACKGROUNDS]
            
            yield Select(options=class_options, prompt="Select Class...", id="char-class")
            yield Select(options=race_options, prompt="Select Race...", id="char-race")
            yield Select(options=bg_options, prompt="Select Background...", id="char-bg")
            
            yield Button("Start Adventure", variant="success", id="btn-start")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start":
            name = self.query_one("#char-name", Input).value.strip() or "Hero"
            
            char_class_select = self.query_one("#char-class", Select).value
            default_class = list(presets.CLASS_STATS.keys())[0]
            char_class = char_class_select if char_class_select != Select.BLANK else default_class
            
            char_race_select = self.query_one("#char-race", Select).value
            default_race = list(presets.RACE_BONUSES.keys())[0]
            char_race = char_race_select if char_race_select != Select.BLANK else default_race
            
            char_bg_select = self.query_one("#char-bg", Select).value
            default_bg = presets.BACKGROUNDS[0]
            char_bg = char_bg_select if char_bg_select != Select.BLANK else default_bg

            self.dismiss((name, char_class, char_race, char_bg))

if __name__ == "__main__":
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    app = DNDGameApp()
    app.run()