from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

# Placeholder map matrix
MAP_DATA = """
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1
1 0 0 E 0 0 0 0 0 1 0 0 0 N 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1
1 1 1 1 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 1
1 0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 2 0 0 2 0 0 P 0 0 0 E 0 0 1
1 0 0 E 0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
"""

class MapScreen(Screen):
    """A screen displaying the game map and legend."""

    CSS_PATH = "map_screen.tcss"

    BINDINGS = [
        ("escape", "close_map", "Back to Main"),
    ]

    def action_close_map(self) -> None:
        self.app.pop_screen()

    def on_mount(self) -> None:
        self.refresh_map()

    def refresh_map(self) -> None:
        map_widget = self.query_one("#map-display", Static)
        map_widget.update(self.app.engine.map_data)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="map-layout"):
            # Left side: The Map
            with Container(id="map-container"):
                yield Static("W O R L D   M A P", classes="section-title")
                yield Static(MAP_DATA.strip(), id="map-display")

            # Right side: The Legend
            with Vertical(id="legend-container"):
                yield Static("L E G E N D", classes="section-title")

                with Vertical(classes="legend-group"):
                    yield Static("## Terrain", classes="legend-category")
                    yield Static("0 - Air / Path", classes="legend-item")
                    yield Static("1 - Stone", classes="legend-item")
                    yield Static("2 - Wood", classes="legend-item")

                with Vertical(classes="legend-group"):
                    yield Static("## Entities", classes="legend-category")
                    yield Static("P - Player Party", classes="legend-item text-player")
                    yield Static("E - Enemy", classes="legend-item text-enemy")
                    yield Static("N - NPC", classes="legend-item text-npc")

        yield Footer()