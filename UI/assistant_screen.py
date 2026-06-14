from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Input

from ai_assistant import PlayerGuideAssistant

class AssistantScreen(Screen):
    """A screen for the player to consult the Game Rules & Mechanics."""
    
    CSS_PATH = "assistant.tcss"

    BINDINGS = [
        ("escape", "close_assistant", "Back to Main"),
        ("ctrl+r", "do_nothing", False), 
        ("ctrl+s", "do_nothing", False),
        ("ctrl+o", "do_nothing", False),
        ("ctrl+g", "do_nothing", False),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guide = PlayerGuideAssistant(model_name="llama3")
        self.chat_log = ["[i]Greetings, traveler. I know the laws of this world intimately. Ask me how anything works![/i]\n"]

    def action_close_assistant(self) -> None:
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="assistant-layout"):
            yield Static("T H E   G U I D E T O M E", classes="section-title")
            with ScrollableContainer(id="assistant-chat-container"):
                yield Static(self.chat_log[0], id="assistant-chat-log")
            yield Input(placeholder="Ask about rules, stats, or mechanics...", id="assistant-input")
        yield Footer()

    @on(Input.Submitted, "#assistant-input")
    def handle_question(self, event: Input.Submitted) -> None:
        question = event.value
        if not question.strip(): return
        
        event.input.value = ""
        self.add_to_log(f"[bold green]You:[/] {question}")
        self.add_to_log("[i yellow]*(Consulting the ancient texts...)*[/]")
        
        self.process_question(question)

    @work(thread=True)
    def process_question(self, question: str) -> None:
        answer = self.guide.ask_question(question)
        self.app.call_from_thread(self.update_answer, answer)

    def update_answer(self, answer: str) -> None:
        self.chat_log.pop() # Remove the thinking message
        self.add_to_log(f"[bold $secondary]Guide:[/] {answer}\n")

    def add_to_log(self, text: str) -> None:
        self.chat_log.append(text)
        log_widget = self.query_one("#assistant-chat-log", Static)
        log_widget.update("\n\n".join(self.chat_log))
        self.query_one("#assistant-chat-container").scroll_end(animate=False)