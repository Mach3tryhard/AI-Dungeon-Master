import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
from UI.tui import DNDGameApp
from textual.widgets import Label

@pytest.mark.asyncio
async def test_app_starts_and_shows_creator():
    app = DNDGameApp()
    
    async with app.run_test() as pilot:
        assert app.title == "AI DM: Dungeons & Dragons"
        
        await pilot.pause(0.1)

        creator_title = app.screen.query_one("#char-creator-title", Label)
        
        assert "CREATE YOUR CHARACTER" in str(creator_title.render())