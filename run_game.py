#!/usr/bin/env python3
"""
Run script for Pride of Code game
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from game import PrideOfCodeGame
    
    if __name__ == "__main__":
        game = PrideOfCodeGame()
        game.run()
        
except ImportError as e:
    print(f"Error importing game module: {e}")
    print("Make sure pygame is installed: pip install pygame")
    sys.exit(1)
except Exception as e:
    print(f"Error running game: {e}")
    sys.exit(1)