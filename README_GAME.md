# Pride of Code - Consolidated Game Implementation

This is the consolidated implementation of the "Pride of Code" game that includes all visual components in a single file.

## Overview

This implementation consolidates all the visual identity components into a single `game.py` file:

1. **Color System** - Complete color palette with all specified colors from the style guide
2. **UI Components** - Reusable UI elements (buttons, panels, score bars) with retro styling
3. **Screen Templates** - Implementations of key screens (Main Menu, Code Editor, Level Select)
4. **Animation System** - Framework for micro-animations (button hovers, score bars, sparkles)
5. **Game Engine** - Main game loop and scene management

## Features Implemented

### Color System
- All primary, secondary, and highlight colors from the style guide
- Color manipulation utilities (brightness adjustment, alpha control)
- Direct access to color constants

### UI Components
- **RetroButton** - Styled buttons with hover, pressed states and glow effects
- **RetroPanel** - Styled panels with customizable borders and backgrounds
- **ScoreBar** - Animated score bars with smooth value transitions
- **TextRenderer** - Pixel-style text rendering with optional outlines

### Screen Templates
- **MainMenuScene** - Main menu with gradient background, crowd silhouettes, and animated star
- **CodeEditorScene** - Code editor with syntax highlighting, error markers, and console
- **LevelSelectScene** - Level selection grid with week badges and competition indicators

### Animation System
- **AnimationManager** - Central manager for all animations
- **ButtonHoverGlow** - Button shimmer effect
- **ScoreBarFill** - Score bar increment animation
- **SparkleEffect** - Pixel sparkles for high scores
- **PixelDissolve** - Transition effects

## Running the Game

To run the game, simply execute:

```bash
python game.py
```

## Controls

- **Main Menu**: Use mouse to click buttons
- **Code Editor**: Use arrow keys to navigate code, Enter to add new lines
- **Level Select**: Click on week tiles to select levels

## File Structure

The game is now contained in a single file:
```
code/
├── game.py              # Complete game implementation
├── README_GAME.md       # This file
├── requirements.txt     # Dependencies
└── ...                  # Other project files (assets, audio, etc.)
```

## Dependencies

- Python 3.11+
- Pygame 2.0+

Install dependencies with:
```bash
pip install pygame
```

## Style Guide Compliance

This implementation follows all specifications from the visual identity style guide:

- **Color System**: All colors match the specified hex values
- **Typography**: Pixel-style text rendering with appropriate sizing
- **Button Design**: Rounded rectangles with proper hover/pressed states
- **Micro-Animations**: Subtle animations that enhance without distraction
- **Screen Layouts**: Proper implementation of all key screen designs

## Customization

All components can be customized:

- **Colors**: Use the provided color constants or create new ones
- **Buttons**: Adjust size, text, and styling
- **Panels**: Customize border colors, background colors, and border width
- **Animations**: Modify timing, colors, and effects