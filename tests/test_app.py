import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
from UI.tui import DNDGameApp
from textual.widgets import Label, Input

@pytest.mark.asyncio
async def test_full_character_creation_flow():
    app = DNDGameApp()
    
    async with app.run_test() as pilot:

        await pilot.pause(0.1)
        
        name_input = app.screen.query_one("#char-name", Input)
        name_input.value = "TestHero"
        
        await pilot.click("#btn-start")
        
        await pilot.pause(0.2)
        
        chat_panel = app.screen.query_one("#chat-panel")
        assert "TestHero" in str(chat_panel.render())
        
        equip_panel = app.screen.query_one("#weapon-info-panel")
        assert "Damage:" in str(equip_panel.render())