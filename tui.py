from textual.app import App, ComposeResult
from textual.containers import Container, Grid, ScrollableContainer
from textual.widgets import Footer, Static, Input
from textual_image.widget import Image

DICE_ART = {
    'd5': r"5",
    'd2': r"2",
    'd20': r"20"
}

STORY_SAMPLE = """
## The Misty Valley
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu neque imperdiet, accumsan metus quis, luctus purus. Fusce felis velit, blandit in dolor accumsan, sollicitudin scelerisque velit. 
Integer eleifend arcu id justo tincidunt, et imperdiet tortor mollis. Sed ac sapien odio. Nulla porttitor, eros luctus tempor placerat, leo odio condimentum augue, vel dapibus lacus nulla vel sem.
Sed in consectetur eros. Nunc dolor mi, feugiat a mauris ac, volutpat euismod libero. Quisque mattis dapibus euismod. Quisque lobortis dolor in orci ultricies fermentum. Donec a risus vel lacus aliquet aliquam.
Aenean efficitur tempus sapien at molestie.
"""

WEAPON_INFO_SAMPLE = """
## Equipment: Longsword
* Damage: 1d8 Slashing
* Weight: 3 kgs
* Properties: Versatile (1d10)
---
This finely balanced blade has seen many battles. A faint rune glow is visible under moonlight.
"""

class DNDGameApp(App):
    """A Textual app to display a D&D DM agent game interface."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        #("c", "push_screen('code')", "Code"),
        #("h", "push_screen('home')", "Home"),
        #("g", "push_screen('game')", "Game"),
        #("p", "push_screen('projects')", "Projects"),
        #("w", "push_screen('widgets')", "Widgets"),
        #("control+s", "push_screen('screenshot')", "Screenshot"),
        #("control+a", "push_screen('maximize')", "Maximize"),
        #("control+p", "push_screen('palette')", "palette"),
    ]

    def compose(self) -> ComposeResult:
        with Grid(id="dnd-main"):
            with Container(id="left-column"):
                yield Image("wizard.jpg", id="wizard-box")
                
                yield Static("--- S T A T S ---", id="stats-separator")
                
                with ScrollableContainer(id="dice-box"):
                    yield Static("Recent Rolls", classes="die")
                    yield Static(DICE_ART['d5'], classes="die")
                    yield Static(DICE_ART['d2'], classes="die")
                    yield Static(DICE_ART['d20'], classes="die")

            with ScrollableContainer(id="right-column"):
                yield Static(STORY_SAMPLE, id="story-panel")
                
                yield Static(WEAPON_INFO_SAMPLE, id="weapon-info-panel")

                yield Input(placeholder="Your action...", id="dm-input")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "AI DM: Dungeons & Dragons"

if __name__ == "__main__":
    app = DNDGameApp()
    app.run()