# Pride of Code Visual Identity Integration Guide

This guide explains how to integrate and use the visual identity components in your game.

## 1. Required Dependencies

The following Python libraries are required:

- `pygame>=2.0.0` - Game framework
- `python>=3.11` - Python version

Install dependencies with:
```bash
pip install pygame
```

## 2. Color System Usage

The color system is implemented in `core/colors.py` and provides all colors from the style guide:

```python
from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, STADIUM_TURF_GREEN, ERROR_RED,
    NEON_COMPETENCE_CYAN, PRECISION_MAGENTA, GOLD_EXCELLENCE
)

# Use colors directly
screen.fill(DARK_GRAPHITE_BLACK)

# Use color palette methods
from core.colors import ColorPalette
darker_blue = ColorPalette.adjust_brightness(DEEP_SIGNAL_BLUE, 0.8)
```

## 3. UI Components Usage

### Buttons

```python
from ui.components import RetroButton

# Create a button
button = RetroButton(100, 100, 200, 50, "CLICK ME")

# Set click callback
button.set_click_callback(lambda: print("Button clicked!"))

# In game loop:
# Handle events
for event in pygame.event.get():
    button.handle_event(event)

# Update
button.update(dt)

# Draw
button.draw(screen)
```

### Panels

```python
from ui.components import RetroPanel

# Create a panel
panel = RetroPanel(50, 50, 300, 200)

# In game loop:
panel.draw(screen)
```

### Score Bars

```python
from ui.components import ScoreBar

# Create a score bar
correctness_bar = ScoreBar(10, 10, 200, 20, STADIUM_TURF_GREEN, "Correctness")

# Set value (automatically animates)
correctness_bar.set_value(85)

# In game loop:
correctness_bar.update(dt)
correctness_bar.draw(screen)
```

## 4. Screen Implementation Examples

### Main Menu

```python
from scenes.main_menu import MainMenuScene

# Create scene
main_menu = MainMenuScene(800, 600)

# In game loop:
# Handle events
for event in pygame.event.get():
    main_menu.handle_event(event)

# Update
main_menu.update(dt)

# Draw
main_menu.draw(screen)
```

### Code Editor

```python
from scenes.code_editor import CodeEditorScene

# Create scene
code_editor = CodeEditorScene(800, 600)

# In game loop:
# Handle events
for event in pygame.event.get():
    code_editor.handle_event(event)

# Update
code_editor.update(dt)

# Draw
code_editor.draw(screen)
```

### Level Select

```python
from scenes.level_select import LevelSelectScene

# Create scene
level_select = LevelSelectScene(800, 600)

# In game loop:
# Handle events
for event in pygame.event.get():
    level_select.handle_event(event)

# Update
level_select.update(dt)

# Draw
level_select.draw(screen)
```

## 5. Animation System Usage

The animation system is implemented in `core/animations.py`:

```python
from core.animations import AnimationManager, SparkleEffect

# Create animation manager
animation_manager = AnimationManager()

# Add animations
sparkle = SparkleEffect(400, 300)
animation_manager.add_animation(sparkle)

# In game loop:
# Update
animation_manager.update(dt)

# Draw
animation_manager.draw(screen)
```

## 6. Text Rendering

The text renderer provides pixel-style text rendering:

```python
from ui.components import TextRenderer

# Create text renderer
text_renderer = TextRenderer()

# Render text
text_surface = text_renderer.render_text(
    "PRIDE OF CODE", 
    style='title', 
    color=GOLD_EXCELLENCE, 
    outline=True
)

# Draw
screen.blit(text_surface, (x, y))
```

## 7. Customization Options

### Color Adjustments

```python
from core.colors import ColorPalette

# Adjust brightness
darker_color = ColorPalette.adjust_brightness(DEEP_SIGNAL_BLUE, 0.7)

# Add transparency
translucent_color = ColorPalette.with_alpha(GOLD_EXCELLENCE, 128)
```

### Button Styling

Buttons automatically follow the style guide, but you can customize:

```python
# Create button with custom font size
button = RetroButton(100, 100, 200, 50, "LARGE BUTTON", font_size=24)
```

## 8. Best Practices

1. **Performance**: Reuse components when possible rather than creating new ones each frame
2. **Memory**: Remove animations from the AnimationManager when they're finished
3. **Consistency**: Use the provided color constants to maintain visual consistency
4. **Scalability**: Use the UIComponent base class for creating new UI elements
5. **Accessibility**: Ensure sufficient contrast using the provided color palette

## 9. File Structure

```
code/
├── core/
│   ├── colors.py          # Color system
│   └── animations.py      # Animation framework
├── ui/
│   └── components.py      # UI components
├── scenes/
│   ├── main_menu.py       # Main menu implementation
│   ├── code_editor.py     # Code editor implementation
│   └── level_select.py    # Level select implementation
└── docs/
    └── visual_integration_guide.md  # This guide
```

## 10. Example Complete Implementation

Here's a complete example showing how to use these components together:

```python
import pygame
import sys
from core.colors import DARK_GRAPHITE_BLACK
from scenes.main_menu import MainMenuScene

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pride of Code")
clock = pygame.time.Clock()

# Create scene
main_menu = MainMenuScene(800, 600)

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        main_menu.handle_event(event)
    
    # Update
    main_menu.update(dt)
    
    # Draw
    screen.fill(DARK_GRAPHITE_BLACK)
    main_menu.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
```

This implementation provides a solid foundation for the visual identity specified in your style guide, with reusable components that can be easily extended or customized as needed.