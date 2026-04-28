from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

class CharacterSheetScreen(Screen):
    """A screen replicating the official D&D character sheet layout."""
    
    CSS_PATH = "sheet.tcss"
    
    BINDINGS = [
        ("escape", "close_sheet", "Back to Main"),
        ("ctrl+r", "do_nothing",False), 
        ("ctrl+s", "do_nothing",False),
        ("ctrl+o", "do_nothing",False),
    ]

    def action_close_sheet(self) -> None:
        self.app.pop_screen()

    def on_mount(self) -> None:
        self.refresh_sheet()

    def refresh_sheet(self) -> None:
        p = self.app.engine.player

        dnd_class_name = getattr(p.dnd_class, "name", "Unknown Class") if hasattr(p, "dnd_class") else "Unknown Class"
        level = getattr(p, "level", 1)
        max_hp = getattr(p, "max_health", getattr(p.dnd_class, "health", 0) if hasattr(p, "dnd_class") else 0)
        speed = getattr(p, "speed", 30)

        self.query_one("#data-char-name", Static).update(getattr(p, "name", "Unknown"))
        self.query_one("#data-class-level", Static).update(f"{dnd_class_name} {level}")
        self.query_one("#data-race", Static).update(getattr(p, "race", "---"))
        self.query_one("#data-background", Static).update(getattr(p, "background", "---"))
        self.query_one("#data-player-name", Static).update(getattr(p, "player_name", "---"))
        self.query_one("#data-alignment", Static).update(getattr(p, "alignment", "---"))
        self.query_one("#data-exp", Static).update(str(getattr(p, "xp", 0)))

        for stat in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
            stat_val = p.stats.get(stat, 10) if hasattr(p, "stats") else 10
            mod_val = p.get_modifier(stat) if hasattr(p, "get_modifier") else 0
            
            self.query_one(f"#score-{stat.lower()}", Static).update(str(stat_val))
            self.query_one(f"#mod-{stat.lower()}", Static).update(f"{mod_val:+d}")

        self.query_one("#data-ac", Static).update(str(getattr(p, "ac", 10)))
        
        init_val = p.get_modifier("DEX") if hasattr(p, "get_modifier") else 0
        self.query_one("#data-init", Static).update(f"{init_val:+d}")
        self.query_one("#data-speed", Static).update(f"{speed} ft")
        self.query_one("#data-hp-cur", Static).update(f"{getattr(p, 'health', 0)} / {max_hp}")
        self.query_one("#data-hp-temp", Static).update(str(getattr(p, "temp_health", 0)))

        inventory_list = getattr(p, "inventory", [])
        if inventory_list:
            inv_text = "\n".join([f"* {item}" for item in inventory_list])
        else:
            inv_text = "Empty"
        self.query_one("#data-equipment", Static).update(inv_text)

        self.query_one("#data-traits", Static).update("---")
        self.query_one("#data-ideals", Static).update("---")
        self.query_one("#data-bonds", Static).update("---")
        self.query_one("#data-flaws", Static).update("---")
        self.query_one("#data-features", Static).update("---")

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with ScrollableContainer(id="character-sheet"):
            with Horizontal(id="header-bar"):
                yield Static("D U N G E O N S   &   D R A G O N S", classes="logo-title")
                
                with Vertical(classes="title-data-field"):
                    yield Static("CHARACTER NAME", classes="field-label")
                    yield Static("", id="data-char-name", classes="field-data")
                    
                with Horizontal(classes="right-header-block"):
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("CLASS & LEVEL", "", "data-class-level")
                        yield self.make_titled_box("RACE", "", "data-race")
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("BACKGROUND", "", "data-background")
                        yield self.make_titled_box("ALIGNMENT", "", "data-alignment")
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("PLAYER NAME", "", "data-player-name")
                        yield self.make_titled_box("EXPERIENCE POINTS", "", "data-exp")
            
            with Horizontal(id="main-body-grid"):
                with Vertical(id="left-column-sheet"):
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("STRENGTH", "mod-str", "score-str")
                        yield self.make_stat_box("DEXTERITY", "mod-dex", "score-dex")
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("CONSTITUTION", "mod-con", "score-con")
                        yield self.make_stat_box("INTELLIGENCE", "mod-int", "score-int")
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("WISDOM", "mod-wis", "score-wis")
                        yield self.make_stat_box("CHARISMA", "mod-cha", "score-cha")
                        
                    yield self.make_titled_box("INSPIRATION", "0")
                    yield self.make_titled_box("PROFICIENCY BONUS", "+2")
                    
                    yield self.make_titled_list("SAVING THROWS", ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"])
                    yield self.make_titled_list("SKILLS", [
                        "Acrobatics (Dex)", "Animal Handling (Wis)", "Arcana (Int)", "Athletics (Str)", "Deception (Cha)",
                        "History (Int)", "Insight (Wis)", "Intimidation (Cha)", "Investigation (Int)", "Medicine (Wis)",
                        "Nature (Int)", "Perception (Wis)", "Performance (Cha)", "Persuasion (Cha)", "Religion (Int)",
                        "Sleight of Hand (Dex)", "Stealth (Dex)", "Survival (Wis)"
                    ])
                    
                    yield self.make_titled_box("PASSIVE WISDOM (PERCEPTION)", "10")
                    yield self.make_titled_text_box("OTHER PROFICIENCIES & LANGUAGES", "Common")

                with Vertical(id="middle-column-sheet"):
                    with Horizontal(id="ac-init-speed-row"):
                        yield self.make_titled_box("ARMOR CLASS", "", "data-ac")
                        yield self.make_titled_box("INITIATIVE", "", "data-init")
                        yield self.make_titled_box("SPEED", "", "data-speed")
                    
                    with Vertical(id="hp-block"):
                        yield Static("Hit Point Maximum", classes="field-label")
                        yield Static("", id="data-hp-cur", classes="field-data hp-data")
                        yield self.make_titled_box("TEMPORARY HIT POINTS", "", "data-hp-temp")
                    
                    with Horizontal(id="hp-adjacent-row"):
                        yield self.make_titled_dice_box()
                        yield self.make_titled_death_saves_box()
                        
                    yield self.make_titled_attacks_section()
                    
                    with Horizontal(id="equipment-block"):
                        with Vertical(id="coin-boxes"):
                            yield self.make_titled_box("CP", "0")
                            yield self.make_titled_box("SP", "0")
                            yield self.make_titled_box("EP", "0")
                            yield self.make_titled_box("GP", "0")
                            yield self.make_titled_box("PP", "0")
                        yield self.make_titled_text_box("EQUIPMENT", "", "data-equipment")

                with Vertical(id="right-column-sheet"):
                    yield self.make_titled_text_box("PERSONALITY TRAITS", "", "data-traits")
                    yield self.make_titled_text_box("IDEALS", "", "data-ideals")
                    yield self.make_titled_text_box("BONDS", "", "data-bonds")
                    yield self.make_titled_text_box("FLAWS", "", "data-flaws")
                    yield self.make_titled_text_box("FEATURES & TRAITS", "", "data-features")

        yield Footer()

    def make_stat_box(self, title, mod_id, score_id):
        return Vertical(
            Static(title, classes="stat-box-title"),
            Static("", id=mod_id, classes="stat-box-modifier"),
            Static("", id=score_id, classes="stat-box-score"),
            classes="stat-box"
        )
    
    def make_titled_box(self, title, placeholder, widget_id=None):
        return Vertical(
            Static(title, classes="field-label"),
            Static(placeholder, id=widget_id, classes="field-data") if widget_id else Static(placeholder, classes="field-data"),
            classes="title-data-field titled-box"
        )

    def make_titled_text_box(self, title, placeholder, widget_id=None):
        return Vertical(
            Static(title, classes="field-label"),
            Static(placeholder, id=widget_id, classes="field-data text-area-placeholder") if widget_id else Static(placeholder, classes="field-data text-area-placeholder"),
            classes="title-data-field titled-text-box"
        )
        
    def make_titled_list(self, title, list_items):
        rows = []
        for item in list_items:
            rows.append(Horizontal(
                Static(item, classes="list-label"), 
                Static("---", classes="field-data list-data"),
                classes="list-row"
            ))
        list_contents = Vertical(*rows, classes="titled-list-contents")
        return Vertical(
            Static(title, classes="field-label"),
            list_contents,
            classes="title-data-field titled-list"
        )

    def make_titled_dice_box(self):
        return Vertical(
            Static("HIT DICE", classes="field-label"),
            Vertical(
                Horizontal(Static("Total", classes="list-label"), Static("1d10", classes="field-data list-data"), classes="list-row"),
                Static("1d10", classes="field-data list-data"),
                classes="hit-dice-contents"
            ),
            classes="title-data-field titled-box"
        )

    def make_titled_death_saves_box(self):
        return Vertical(
            Static("DEATH SAVES", classes="field-label"),
            Vertical(
                Horizontal(Static("SUCCESSES", classes="list-label"), Static("[ ] [ ] [ ]", classes="field-data list-data death-save-circles"), classes="list-row"),
                Horizontal(Static("FAILURES", classes="list-label"), Static("[ ] [ ] [ ]", classes="field-data list-data death-save-circles"), classes="list-row"),
                classes="death-saves-contents"
            ),
            classes="title-data-field titled-box"
        )

    def make_titled_attacks_section(self):
        return Vertical(
            Static("ATTACKS & SPELLCASTING", classes="field-label"),
            Horizontal(
                Static("NAME", classes="subheader"),
                Static("ATK BONUS", classes="subheader"),
                Static("DAMAGE/TYPE", classes="subheader"),
                classes="attacks-subheaders"
            ),
            Static("---", classes="field-data text-area-placeholder"),
            classes="title-data-field attacks-section"
        )