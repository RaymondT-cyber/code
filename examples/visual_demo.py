"""
Pride of Code Visual Identity Demo
==================================

Demonstration of all visual components working together.
"""

import pygame
import sys
import os
import math

# Add the code directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, NEON_COMPETENCE_CYAN, GOLD_EXCELLENCE,
    PRECISION_MAGENTA, STADIUM_TURF_GREEN
)
from ui.components import RetroButton, RetroPanel, ScoreBar, TextRenderer
from core.animations import AnimationManager, SparkleEffect
from scenes.main_menu import MainMenuScene
from scenes.code_editor import CodeEditorScene
from scenes.level_select import LevelSelectScene


class VisualDemo:
    """Demo application showcasing all visual components."""
    
    def __init__(self):
        pygame.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pride of Code - Visual Identity Demo")
        self.clock = pygame.time.Clock()
        
        # Demo state
        self.current_demo = "main_menu"  # main_menu, code_editor, level_select, components
        self.demo_scenes = {}
        
        # Create demo scenes
        self._create_demo_scenes()
        
        # Create component demo elements
        self._create_component_demo()
        
        # Font for demo labels
        self.font = pygame.font.Font(None, 24)
    
    def _create_demo_scenes(self):
        """Create instances of all demo scenes."""
        self.demo_scenes["main_menu"] = MainMenuScene(self.screen_width, self.screen_height)
        self.demo_scenes["code_editor"] = CodeEditorScene(self.screen_width, self.screen_height)
        self.demo_scenes["level_select"] = LevelSelectScene(self.screen_width, self.screen_height)
    
    def _create_component_demo(self):
        """Create individual components for the component demo."""
        # Create buttons
        self.demo_buttons = [
            RetroButton(50, 100, 200, 50, "NORMAL BUTTON"),
            RetroButton(300, 100, 200, 50, "HOVER BUTTON"),
            RetroButton(550, 100, 200, 50, "PRESSED BUTTON")
        ]
        
        # Set states for demo purposes
        self.demo_buttons[1].state = "hover"
        self.demo_buttons[1].glow_alpha = 1.0
        self.demo_buttons[2].state = "pressed"
        self.demo_buttons[2].pressed_offset = 1
        
        # Create panels
        self.demo_panels = [
            RetroPanel(50, 200, 300, 150),
            RetroPanel(400, 200, 300, 150, border_color=GOLD_EXCELLENCE, background_color=pygame.Color(26, 28, 30, 200))
        ]
        
        # Create score bars
        self.demo_score_bars = [
            ScoreBar(50, 400, 200, 20, STADIUM_TURF_GREEN, "Correctness"),
            ScoreBar(50, 450, 200, 20, PRECISION_MAGENTA, "Creativity"),
            ScoreBar(50, 500, 200, 20, NEON_COMPETENCE_CYAN, "Performance")
        ]
        
        # Set values for demo
        self.demo_score_bars[0].set_value(85)
        self.demo_score_bars[1].set_value(72)
        self.demo_score_bars[2].set_value(93)
        
        # Animation manager
        self.animation_manager = AnimationManager()
        
        # Text renderer
        self.text_renderer = TextRenderer()
        
        # Navigation buttons
        self.nav_buttons = [
            RetroButton(50, 650, 150, 40, "Main Menu"),
            RetroButton(220, 650, 150, 40, "Code Editor"),
            RetroButton(390, 650, 150, 40, "Level Select"),
            RetroButton(560, 650, 150, 40, "Components")
        ]
        
        # Set callbacks
        self.nav_buttons[0].set_click_callback(lambda: setattr(self, 'current_demo', 'main_menu'))
        self.nav_buttons[1].set_click_callback(lambda: setattr(self, 'current_demo', 'code_editor'))
        self.nav_buttons[2].set_click_callback(lambda: setattr(self, 'current_demo', 'level_select'))
        self.nav_buttons[3].set_click_callback(lambda: setattr(self, 'current_demo', 'components'))
        
        # Add some sparkle effects for demo
        sparkle1 = SparkleEffect(800, 300, count=8)
        sparkle2 = SparkleEffect(900, 400, count=6)
        self.animation_manager.add_animation(sparkle1)
        self.animation_manager.add_animation(sparkle2)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle navigation buttons
            for button in self.nav_buttons:
                button.handle_event(event)
            
            # Handle current demo scene
            if self.current_demo in self.demo_scenes:
                self.demo_scenes[self.current_demo].handle_event(event)
            elif self.current_demo == "components":
                # Handle component demo buttons
                for button in self.demo_buttons:
                    button.handle_event(event)
            
            # Add sparkle on click for component demo
            if self.current_demo == "components" and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    sparkle = SparkleEffect(event.pos[0], event.pos[1], count=5)
                    self.animation_manager.add_animation(sparkle)
        
        return True
    
    def update(self, dt):
        """Update demo state."""
        # Update current scene
        if self.current_demo in self.demo_scenes:
            self.demo_scenes[self.current_demo].update(dt)
        elif self.current_demo == "components":
            # Update component demo elements
            for button in self.demo_buttons:
                button.update(dt)
            
            for bar in self.demo_score_bars:
                bar.update(dt)
            
            self.animation_manager.update(dt)
        
        # Update navigation buttons
        for button in self.nav_buttons:
            button.update(dt)
    
    def draw_components_demo(self):
        """Draw the components demo screen."""
        # Draw title
        title = self.text_renderer.render_text(
            "UI COMPONENTS DEMO", 
            style='title', 
            color=GOLD_EXCELLENCE, 
            outline=True
        )
        title_rect = title.get_rect(center=(self.screen_width // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw buttons section label
        buttons_label = self.font.render("Buttons:", True, SILVER_STEEL)
        self.screen.blit(buttons_label, (50, 70))
        
        # Draw buttons
        for button in self.demo_buttons:
            button.draw(self.screen)
        
        # Draw panels section label
        panels_label = self.font.render("Panels:", True, SILVER_STEEL)
        self.screen.blit(panels_label, (50, 170))
        
        # Draw panels
        for panel in self.demo_panels:
            panel.draw(self.screen)
        
        # Add some content to panels
        panel_text1 = self.font.render("Standard Panel", True, SILVER_STEEL)
        panel_text2 = self.font.render("Custom Styled Panel", True, GOLD_EXCELLENCE)
        self.screen.blit(panel_text1, (60, 210))
        self.screen.blit(panel_text2, (410, 210))
        
        # Draw score bars section label
        bars_label = self.font.render("Score Bars:", True, SILVER_STEEL)
        self.screen.blit(bars_label, (50, 370))
        
        # Draw score bars
        for bar in self.demo_score_bars:
            bar.draw(self.screen)
        
        # Draw color palette demo
        self._draw_color_palette()
        
        # Draw animations
        self.animation_manager.draw(self.screen)
    
    def _draw_color_palette(self):
        """Draw the color palette for reference."""
        colors = [
            ("DARK_GRAPHITE_BLACK", DARK_GRAPHITE_BLACK),
            ("RETRO_PIXEL_AMBER", RETRO_PIXEL_AMBER),
            ("DEEP_SIGNAL_BLUE", DEEP_SIGNAL_BLUE),
            ("SILVER_STEEL", SILVER_STEEL),
            ("STADIUM_TURF_GREEN", STADIUM_TURF_GREEN),
            ("ERROR_RED", pygame.Color(194, 55, 55)),
            ("NEON_COMPETENCE_CYAN", NEON_COMPETENCE_CYAN),
            ("PRECISION_MAGENTA", PRECISION_MAGENTA),
            ("GOLD_EXCELLENCE", GOLD_EXCELLENCE)
        ]
        
        # Draw color palette label
        palette_label = self.font.render("Color Palette:", True, SILVER_STEEL)
        self.screen.blit(palette_label, (500, 200))
        
        # Draw color swatches
        for i, (name, color) in enumerate(colors):
            x = 500
            y = 240 + i * 30
            
            # Draw color swatch
            pygame.draw.rect(self.screen, color, (x, y, 20, 20))
            pygame.draw.rect(self.screen, SILVER_STEEL, (x, y, 20, 20), 1)
            
            # Draw color name
            name_text = self.font.render(name, True, SILVER_STEEL)
            self.screen.blit(name_text, (x + 30, y + 2))
    
    def draw(self):
        """Draw the current demo screen."""
        # Clear screen
        self.screen.fill(DARK_GRAPHITE_BLACK)
        
        # Draw current demo
        if self.current_demo in self.demo_scenes:
            self.demo_scenes[self.current_demo].draw(self.screen)
        elif self.current_demo == "components":
            self.draw_components_demo()
        
        # Draw navigation buttons at the bottom
        for button in self.nav_buttons:
            button.draw(self.screen)
        
        # Draw current demo label
        demo_label = self.font.render(f"Current Demo: {self.current_demo.replace('_', ' ').title()}", True, NEON_COMPETENCE_CYAN)
        self.screen.blit(demo_label, (50, 20))
    
    def run(self):
        """Run the demo application."""
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    demo = VisualDemo()
    demo.run()