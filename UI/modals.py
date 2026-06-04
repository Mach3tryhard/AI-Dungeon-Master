from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.containers import Vertical, Horizontal

class AttackConfirmationModal(ModalScreen[bool]):
    def __init__(self, target: str, weapon_name: str, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.weapon_name = weapon_name

    def compose(self):
        with Vertical(id="modal-dialog"):
            yield Static("=== PREPARE FOR BATTLE ===", id="modal-title")
            
            yield Static(f"Target: [bold red]{self.target}[/]\nWeapon: [bold cyan]{self.weapon_name}[/]", id="modal-text")
            
            with Horizontal(id="modal-buttons"):
                yield Button("Roll to Attack!", variant="success", id="btn-confirm")
                yield Button("Retreat", variant="error", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)