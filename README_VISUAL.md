# Pride of Code Visual Identity Implementation

This repository contains the complete visual identity implementation for the "Pride of Code" game, following the style guide specifications.

## Overview

This implementation provides:

1. **Color System** - Complete color palette with all specified colors from the style guide
2. **UI Components** - Reusable UI elements (buttons, panels, score bars) with retro styling
3. **Screen Templates** - Implementations of key screens (Main Menu, Code Editor, Level Select)
4. **Animation System** - Framework for micro-animations (button hovers, score bars, sparkles)
5. **Typography System** - Text rendering with pixel-style styling

## Features Implemented

### Color System (`core/colors.py`)
- All primary, secondary, and highlight colors from the style guide
- Color manipulation utilities (brightness adjustment, alpha control)
- Direct access to color constants

### UI Components (`ui/components.py`)
- **RetroButton** - Styled buttons with hover, pressed states and glow effects
- **RetroPanel** - Styled panels with customizable borders and backgrounds
- **ScoreBar** - Animated score bars with smooth value transitions
- **TextRenderer** - Pixel-style text rendering with optional outlines

### Screen Templates (`scenes/`)
- **MainMenuScene** - Main menu with gradient background, crowd silhouettes, and animated star
- **CodeEditorScene** - Code editor with syntax highlighting, error markers, and console
- **LevelSelectScene** - Level selection grid with week badges and competition indicators

### Animation System (`core/animations.py`)
- **AnimationManager** - Central manager for all animations
- **ButtonHoverGlow** - Button shimmer effect
- **ScoreBarFill** - Score bar increment animation
- **SparkleEffect** - Pixel sparkles for high scores
- **PixelDissolve** - Transition effects

## Style Guide Compliance

This implementation follows all specifications from the visual identity style guide:

- **Color System**: All colors match the specified hex values
- **Typography**: Pixel-style text rendering with appropriate sizing
- **Button Design**: Rounded rectangles with proper hover/pressed states
- **Micro-Animations**: Subtle animations that enhance without distraction
- **Screen Layouts**: Proper implementation of all key screen designs

## Installation

```bash
# Install required dependencies
pip install pygame
```

## Usage

### Basic Usage
```python
from core.colors import DARK_GRAPHITE_BLACK, DEEP_SIGNAL_BLUE
from ui.components import RetroButton

# Create a button
button = RetroButton(100, 100, 200, 50, "CLICK ME")
button.set_click_callback(lambda: print("Clicked!"))

# In game loop
for event in pygame.event.get():
    button.handle_event(event)

button.update(dt)
button.draw(screen)
```

### Screen Implementation
```python
from scenes.main_menu import MainMenuScene

# Create scene
main_menu = MainMenuScene(800, 600)

# In game loop
main_menu.handle_event(event)
main_menu.update(dt)
main_menu.draw(screen)
```

## File Structure

```
code/
├── core/
│   ├── colors.py          # Color system implementation
│   └── animations.py      # Animation framework
├── ui/
│   └── components.py      # UI components
├── scenes/
│   ├── main_menu.py       # Main menu screen
│   ├── code_editor.py     # Code editor screen
│   └── level_select.py    # Level select screen
├── examples/
│   └── visual_demo.py     # Demo application
├── tests/
│   └── test_visual_components.py  # Test suite
├── docs/
│   └── visual_integration_guide.md  # Integration guide
├── README_VISUAL.md       # This file
```

## Testing

Run the test suite to verify all components are working:

```bash
cd code
python tests/test_visual_components.py
```

## Demo

Run the visual demo to see all components in action:

```bash
cd code
python examples/visual_demo.py
```

## Integration Guide

See `docs/visual_integration_guide.md` for detailed instructions on integrating these components into your game.

## Customization

All components can be customized:

- **Colors**: Use the provided color constants or create new ones
- **Buttons**: Adjust size, text, and styling
- **Panels**: Customize border colors, background colors, and border width
- **Animations**: Modify timing, colors, and effects

## Dependencies

- Python 3.11+
- Pygame 2.0+

## Style Guide References

This implementation follows these sections of the visual identity style guide:

1. Visual Identity Style Pillars
2. Color System Specification
3. Typography Specification
4. Micro-Detail Visual Rules
5. Screen-Specific Visual Design
6. Animation Guidelines
7. Shadow & Lighting Rules
8. Audio-Visual Cohesion

## Contributing

To extend or modify the visual components:

1. Follow the existing code style
2. Maintain consistency with the style guide
3. Add tests for new functionality
4. Update the documentation as needed

## License

This implementation is provided as part of the Pride of Code game development and is intended for use in that project.