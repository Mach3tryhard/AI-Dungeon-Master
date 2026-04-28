import sys
import os
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, ScrollableContainer
from textual.widgets import Footer, Static, Input
from textual.reactive import reactive
import random
from textual.widgets import Header, Footer, Static
from engine import GameEngine
from ai_dm import AIDungeonMaster

from map_screen import MapScreen
from sheet import CharacterSheetScreen

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


DICE_SHAPES = {
    "d4": (
        "          \n"
        "    /\\    \n"
        "   /  \\   \n"
        "  /    \\  \n"
        " /  {val}  \\ \n"
        "/________\\ "
    ),
    "d6": (
        "          \n"
        " ┌──────┐ \n"
        " │      │ \n"
        " │  {val}  │ \n"
        " │      │ \n"
        " └──────┘ "
    ),
    "d8": (
        "    /\\    \n"
        "   /  \\   \n"
        "  /____\\  \n"
        "  \\ {val} /  \n"
        "   \\  /   \n"
        "    \\/    "
    ),
    "d10": (
        "   ____    \n"
        "  / || \\  \n"
        " /  {val}  \\ \n"
        " \\  ||  / \n"
        "  \\_||_/  "
    ),
    "d12": (
        "   ____   \n"
        "  / __ \\  \n"
        " / /  \ \\ \n"
        "| | {val} | |\n"
        " \\ \__/ / \n"
        "  \\____/  "
    ),
    "d20": (
        "   ____   \n"
        "  /\\  /\\  \n"
        " /  \\/  \\ \n"
        " \\  {val}  / \n"
        "  \\    /  \n"
        "   \\__/   "
    )
}

# --- Custom ASCII Dice Widget ---

class AsciiDie(Static):
    def __init__(self, die_type: str, final_value: int, **kwargs):
        super().__init__(**kwargs)
        self.die_type = die_type
        self.final_value = final_value
        self.ticks = 0
        self.max_ticks = 15
        
        self.template = DICE_SHAPES.get(self.die_type, DICE_SHAPES["d6"])

    def on_mount(self) -> None:
        self.animation_timer = self.set_interval(1 / 15, self.animate_roll)

    def animate_roll(self) -> None:
        self.ticks += 1
        
        if self.ticks < self.max_ticks:
            
            fake_val = random.randint(1, 20)
            self.draw_face(fake_val)
        else:
            
            self.draw_face(self.final_value)
            self.animation_timer.pause()

    def draw_face(self, value: int) -> None:
        
        val_str = f"{value:>2}" 

        art = self.template.format(val=val_str)
        
        self.update(f"[bold $primary]{art}[/]")


# --- App Logic ---

class DNDGameApp(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("ctrl+s", "show_sheet", "Open Character Sheet"),
        ("ctrl+o", "show_map", "Open Map"),
        ("ctrl+r", "roll_test", "Test Roll"), 
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Grid(id="dnd-main"):
            with Container(id="left-column"):
                yield Static("DUNGEON MASTER", id="dm-title")  

                yield Static(ASCII_WIZARD, id="wizard-box")
                
                yield Static("DICE BOX", id="stats-separator")
                
                with Container(id="dice-area"):
                    yield Static("Total Sum: --, Dice: --", id="total-display")
                    
                    with Grid(id="dice-box"):
                        pass 

            with ScrollableContainer(id="right-column"):
                yield Static("## The Story\nYour journey begins...", id="story-panel")
                yield Static("## Action Log\n", id="chat-panel")
                yield Static("## Equipment", id="weapon-info-panel")
                yield Input(placeholder="Your action...", id="dm-input")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "AI DM: Dungeons & Dragons"
        self.engine = GameEngine()
        self.ai_dm = AIDungeonMaster(model_name="llama3")
        
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
        story_panel = self.query_one("#story-panel", Static)
        story_panel.update("## The Story\n" + "\n\n".join(self.engine.story_log))

        chat_panel = self.query_one("#chat-panel", Static)
        chat_text = "\n".join(self.engine.chat_log)
        
        if getattr(self.engine, "is_thinking", False):
            chat_text += "\n\n[i yellow]*(The DM is rolling dice and thinking...)*[/]"
            
        chat_panel.update("## Action Log\n" + chat_text)

    def update_equipment_display(self) -> None:
        equip_panel = self.query_one("#weapon-info-panel", Static)
        full_equip = "\n".join(self.engine.player.inventory)
        equip_panel.update(f"## Equipment\n{full_equip}")

    @on(Input.Submitted, "#dm-input")
    def handle_player_action(self, event: Input.Submitted) -> None:
        player_text = event.value
        if not player_text.strip(): return
        
        event.input.value = "" 
        
        self.engine.chat_log.append(f"[bold green]You:[/] {player_text}")
        
        self.engine.is_thinking = True
        self.update_story_display()
        
        self.process_turn_background(player_text)

    @work(thread=True)
    def process_turn_background(self, player_text: str) -> None:
        intent = self.ai_dm.parse_intent(player_text)
        engine_result = self.engine.process_action(intent,ai_dm=self.ai_dm)
        narrative = self.ai_dm.narrate_outcome(player_text, engine_result)
        
        self.app.call_from_thread(self.finalize_turn, narrative)

    def finalize_turn(self, narrative: str) -> None:
        self.engine.is_thinking = False
        
        self.engine.chat_log.append(f"[bold $secondary]DM:[/] {narrative}")
        
        self.engine.add_story(narrative) 
        
        self.update_story_display()

    def roll_dice(self, die_type: str, outcomes: list[int]) -> None:
        
        dice_box = self.query_one("#dice-box")
        total_display = self.query_one("#total-display", Static)

        for child in dice_box.children:
            child.remove()

        total_sum = sum(outcomes)
        total_display.update(f"Total Sum: {total_sum}, Dice: {die_type}")

        for value in outcomes[:9]:
            dice_box.mount(AsciiDie(die_type, final_value=value, classes="die"))

    def action_roll_test(self) -> None:
        self.roll_dice(random.choice(dice), [random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)])
    def action_show_sheet(self) -> None:
        if not isinstance(self.screen, CharacterSheetScreen):
            self.push_screen(CharacterSheetScreen())
    def action_show_map(self) -> None:
        if not isinstance(self.screen, MapScreen):
            self.push_screen(MapScreen())

if __name__ == "__main__":
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    app = DNDGameApp()
    app.run()