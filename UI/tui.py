from textual.app import App, ComposeResult
from textual.containers import Container, Grid, ScrollableContainer
from textual.widgets import Footer, Static, Input
from textual.reactive import reactive
import random
from textual.widgets import Header, Footer, Static

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
    """An ASCII die that animates random numbers before landing on a final outcome."""

    def __init__(self, die_type: str, final_value: int, **kwargs):
        super().__init__(**kwargs)
        self.die_type = die_type
        self.final_value = final_value
        self.ticks = 0
        self.max_ticks = 15
        
        self.template = DICE_SHAPES.get(self.die_type, DICE_SHAPES["d6"])

    def on_mount(self) -> None:
        """Start the animation loop at 15 frames per second."""
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
        """Formats the ASCII string with the number and updates the widget."""
        
        val_str = f"{value:>2}" 
        art = self.template.format(val=val_str)
        
        self.update(f"[bold $primary]{art}[/]")


# --- App Logic ---

class DNDGameApp(App):
    """A Textual app to display a D&D DM agent game interface."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("r", "roll_test", "Test Roll"), 
        ("c", "show_sheet", "Open Character Sheet"),
        ("m", "show_map", "Open Map"),
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
                yield Static("## Equipment", id="weapon-info-panel")
                yield Input(placeholder="Your action...", id="dm-input")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "AI DM: Dungeons & Dragons"

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
    app = DNDGameApp()
    app.run()