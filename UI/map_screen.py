from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

class MapScreen(Screen):
    CSS_PATH = "map_screen.tcss"

    BINDINGS = [
        ("escape", "close_map", "Back to Main"),
        ("ctrl+r", "do_nothing",False), 
        ("ctrl+s", "do_nothing",False),
        ("ctrl+o", "do_nothing",False),
        ("ctrl+g", "do_nothing", False),
    ]

    def action_close_map(self) -> None:
        self.app.pop_screen()

    def on_mount(self) -> None:
        self.refresh_map()

    def refresh_map(self) -> None:
        map_widget = self.query_one("#map-display", Static)

        matrix = self.app.engine.map_class.full_map
        map_display = "\n".join(" ".join(str(cell) for cell in row) for row in matrix)
        map_widget.update(map_display)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="map-layout"):

            with Container(id="map-container"):
                yield Static("W O R L D   M A P", classes="section-title")
                yield Static("", id="map-display")

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