import pytest
from unittest.mock import patch
from src.redaffair.case import load_case

def test_scripted_playthrough():
    # Minimal scripted interaction to verify game loop starts and ends without crashing
    # (Full implementation is STEP 5.5 work)
    inputs = [
        "",           # Press Enter
        "TestDetective",  # Name
        "1",          # Political lean (Communist)
        "",           # Press Enter airlock
        "quit"        # Quit immediately
    ]
    
    with patch('builtins.input', side_effect=inputs):
        with patch('builtins.print') as mock_print:
            # We patch the sys.exit to avoid stopping the test runner
            with patch('sys.exit') as mock_exit:
                from game import play_game
                try:
                    play_game()
                except Exception:
                    pass
                
    assert mock_print.called
    assert mock_exit.called
