from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

class CharacterSheetScreen(Screen):
    """A screen replicating the official D&D character sheet layout."""
    
    CSS_PATH = "sheet.tcss"
    
    BINDINGS = [
        ("escape", "close_sheet", "Back to Main"),
    ]

    def action_close_sheet(self) -> None:
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with ScrollableContainer(id="character-sheet"):
            with Horizontal(id="header-bar"):
                yield Static("D U N G E O N S   &   D R A G O N S", classes="logo-title")
                
                with Vertical(classes="title-data-field"):
                    yield Static("CHARACTER NAME", classes="field-label")
                    yield Static("Character Name Data Area", classes="field-data")
                    
                with Horizontal(classes="right-header-block"):
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("CLASS & LEVEL", "Class Data")
                        yield self.make_titled_box("RACE", "Race Data")
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("BACKGROUND", "Background Data")
                        yield self.make_titled_box("ALIGNMENT", "Alignment Data")
                    with Vertical(classes="header-column"):
                        yield self.make_titled_box("PLAYER NAME", "Player Name Data")
                        yield self.make_titled_box("EXPERIENCE POINTS", "XP Data Area")
            
            with Horizontal(id="main-body-grid"):
                
                with Vertical(id="left-column-sheet"):
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("STRENGTH", "Str Mod", "Str Score")
                        yield self.make_stat_box("DEXTERITY", "Dex Mod", "Dex Score")
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("CONSTITUTION", "Con Mod", "Con Score")
                        yield self.make_stat_box("INTELLIGENCE", "Int Mod", "Int Score")
                    with Horizontal(classes="stat-box-row"):
                        yield self.make_stat_box("WISDOM", "Wis Mod", "Wis Score")
                        yield self.make_stat_box("CHARISMA", "Cha Mod", "Cha Score")
                        
                    yield self.make_titled_box("INSPIRATION", "Inspiration Data Area")
                    yield self.make_titled_box("PROFICIENCY BONUS", "Bonus Data Area")
                    
                    yield self.make_titled_list("SAVING THROWS", ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"])
                    yield self.make_titled_list("SKILLS", [
                        "Acrobatics (Dex)", "Animal Handling (Wis)", "Arcana (Int)", "Athletics (Str)", "Deception (Cha)",
                        "History (Int)", "Insight (Wis)", "Intimidation (Cha)", "Investigation (Int)", "Medicine (Wis)",
                        "Nature (Int)", "Perception (Wis)", "Performance (Cha)", "Persuasion (Cha)", "Religion (Int)",
                        "Sleight of Hand (Dex)", "Stealth (Dex)", "Survival (Wis)"
                    ])
                    
                    yield self.make_titled_box("PASSIVE WISDOM (PERCEPTION)", "Passive Perc. Data Area")
                    yield self.make_titled_text_box("OTHER PROFICIENCIES & LANGUAGES", "Languages / Proficiencies Data Area")

                with Vertical(id="middle-column-sheet"):
                    with Horizontal(id="ac-init-speed-row"):
                        yield self.make_titled_box("ARMOR CLASS", "AC Data Area")
                        yield self.make_titled_box("INITIATIVE", "Init Data Area")
                        yield self.make_titled_box("SPEED", "Speed Data Area")
                    
                    with Vertical(id="hp-block"):
                        yield Static("Hit Point Maximum", classes="field-label")
                        yield Static("HP Max Data Area", classes="field-data hp-data")
                        yield self.make_titled_box("CURRENT HIT POINTS", "Current HP Data Area")
                        yield self.make_titled_box("TEMPORARY HIT POINTS", "Temp HP Data Area")
                    
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
                        yield self.make_titled_text_box("EQUIPMENT", "Large text for items & gold...")

                with Vertical(id="right-column-sheet"):
                    yield self.make_titled_text_box("PERSONALITY TRAITS", "Traits Data Area")
                    yield self.make_titled_text_box("IDEALS", "Ideals Data Area")
                    yield self.make_titled_text_box("BONDS", "Bonds Data Area")
                    yield self.make_titled_text_box("FLAWS", "Flaws Data Area")
                    yield self.make_titled_text_box("FEATURES & TRAITS", "Features Data Area")

        yield Footer()

    def make_stat_box(self, title, mod_placeholder, score_placeholder):
        return Vertical(
            Static(title, classes="stat-box-title"),
            Static(mod_placeholder, classes="stat-box-modifier"),
            Static(score_placeholder, classes="stat-box-score"),
            classes="stat-box"
        )
    
    def make_titled_box(self, title, placeholder):
        return Vertical(
            Static(title, classes="field-label"),
            Static(placeholder, classes="field-data"),
            classes="title-data-field titled-box"
        )

    def make_titled_text_box(self, title, placeholder):
        return Vertical(
            Static(title, classes="field-label"),
            Static(placeholder, classes="field-data text-area-placeholder"),
            classes="title-data-field titled-text-box"
        )
        
    def make_titled_list(self, title, list_items):
        rows = []
        for item in list_items:
            rows.append(Horizontal(
                Static(item, classes="list-label"), 
                Static("Data Area", classes="field-data list-data"),
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
                Horizontal(Static("Total", classes="list-label"), Static("Total Data", classes="field-data list-data"), classes="list-row"),
                Static("Dice Data Area", classes="field-data list-data"),
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
            Static("Large attacks & spells text data area...", classes="field-data text-area-placeholder"),
            classes="title-data-field attacks-section"
        )