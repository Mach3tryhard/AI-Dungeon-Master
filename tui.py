import os
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, ScrollableContainer
from textual.widgets import Footer, Static, Input
from textual.reactive import reactive
from textual_image.widget import Image
from PIL import Image as PILImage, ImageSequence

class AnimatedGif(Container):
    """A custom widget that plays a GIF like a flipbook."""

    # Removed the 'height' parameter here
    def __init__(self, gif_path: str, fps: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.gif_path = gif_path
        self.fps = fps
        self.frames = []
        self.current_frame_index = 0
        
        if os.path.exists(self.gif_path):
            with PILImage.open(self.gif_path) as img:
                for frame in ImageSequence.Iterator(img):
                    self.frames.append(frame.convert("RGBA"))

    def compose(self) -> ComposeResult:
        if self.frames:
            self.img_widget = Image(self.frames[0])
            yield self.img_widget
        else:
            yield Static(f"[red]Error loading {self.gif_path}[/]")

    def on_mount(self) -> None:
        """Start the animation timer when the widget appears."""
        # Removed the self.styles lines from here!
        
        if self.frames:
            self.set_interval(1 / self.fps, self.next_frame)

    def next_frame(self) -> None:
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.img_widget.image = self.frames[self.current_frame_index]

DICE_ART = {
    'd5': r"5",
    'd2': r"2",
    'd20': r"20"
}

STORY_SAMPLE = """
The Misty Valley
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eu neque imperdiet, accumsan metus quis, luctus purus. Fusce felis velit, blandit in dolor accumsan, sollicitudin scelerisque velit. 
Integer eleifend arcu id justo tincidunt, et imperdiet tortor mollis. Sed ac sapien odio. Nulla porttitor, eros luctus tempor placerat, leo odio condimentum augue, vel dapibus lacus nulla vel sem.
Sed in consectetur eros. Nunc dolor mi, feugiat a mauris ac, volutpat euismod libero. Quisque mattis dapibus euismod. Quisque lobortis dolor in orci ultricies fermentum. Donec a risus vel lacus aliquet aliquam.
Aenean efficitur tempus sapien at molestie.
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

    theme = "gruvbox"

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
                    #yield Static("[bold $secondary]Recent Rolls[/]", classes="die")
                    
                    yield AnimatedGif("d4_trans.gif", fps=12, classes="die")

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
    print("TEST")