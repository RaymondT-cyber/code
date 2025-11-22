"""
Pride of Code Main Menu Screen
==============================

Implementation of the main menu following the visual identity style guide.

Style Guide Reference:
Section 5.1 Main Menu Screen
"""

import pygame
import math
from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, NEON_COMPETENCE_CYAN, GOLD_EXCELLENCE
)
from ui.components import RetroButton, TextRenderer
from core.animations import SparkleEffect, AnimationManager


class MainMenuScene:
    """
    Main menu screen implementation.
    
    Style Guide Reference:
    Section 5.1 Main Menu Screen
    """
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.animation_manager = AnimationManager()
        self.text_renderer = TextRenderer()
        
        # Background gradient colors
        self.top_color = pygame.Color(39, 48, 65)  # #273041
        self.bottom_color = DARK_GRAPHITE_BLACK   # #1A1C1E
        
        # Crowd silhouette properties
        self.crowd_offset = 0
        self.crowd_speed = 10  # pixels per second
        
        # Star animation
        self.star_timer = 0
        self.star_visible = False
        
        self._create_buttons()
    
    def _create_buttons(self):
        """Create the main menu buttons."""
        button_width = 300
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        
        # Play button
        play_button = RetroButton(
            button_x, 
            self.screen_height // 2 - 60, 
            button_width, 
            button_height, 
            "PLAY GAME"
        )
        play_button.set_click_callback(self._on_play_clicked)
        self.buttons.append(play_button)
        
        # Level Select button
        level_button = RetroButton(
            button_x, 
            self.screen_height // 2 + 10, 
            button_width, 
            button_height, 
            "LEVEL SELECT"
        )
        level_button.set_click_callback(self._on_level_select_clicked)
        self.buttons.append(level_button)
        
        # Settings button
        settings_button = RetroButton(
            button_x, 
            self.screen_height // 2 + 80, 
            button_width, 
            button_height, 
            "SETTINGS"
        )
        settings_button.set_click_callback(self._on_settings_clicked)
        self.buttons.append(settings_button)
        
        # Quit button
        quit_button = RetroButton(
            button_x, 
            self.screen_height // 2 + 150, 
            button_width, 
            button_height, 
            "QUIT"
        )
        quit_button.set_click_callback(self._on_quit_clicked)
        self.buttons.append(quit_button)
    
    def _on_play_clicked(self):
        """Handle play button click."""
        print("Play button clicked")
        # In a real implementation, this would transition to the game scene
    
    def _on_level_select_clicked(self):
        """Handle level select button click."""
        print("Level select button clicked")
        # In a real implementation, this would transition to the level select scene
    
    def _on_settings_clicked(self):
        """Handle settings button click."""
        print("Settings button clicked")
        # In a real implementation, this would transition to the settings scene
    
    def _on_quit_clicked(self):
        """Handle quit button click."""
        print("Quit button clicked")
        # In a real implementation, this would exit the game
    
    def _draw_background(self, surface):
        """Draw the gradient background with crowd silhouettes."""
        # Draw gradient background
        for y in range(self.screen_height):
            # Calculate interpolation factor
            factor = y / self.screen_height
            r = int(self.bottom_color.r * (1 - factor) + self.top_color.r * factor)
            g = int(self.bottom_color.g * (1 - factor) + self.top_color.g * factor)
            b = int(self.bottom_color.b * (1 - factor) + self.top_color.b * factor)
            
            pygame.draw.line(surface, (r, g, b), (0, y), (self.screen_width, y))
        
        # Draw crowd silhouettes (simplified implementation)
        crowd_color = pygame.Color(0, 0, 0, int(255 * 0.1))  # 10% opacity
        crowd_surface = pygame.Surface((self.screen_width, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(crowd_surface, crowd_color, (0, 0, 100, 30))
        pygame.draw.ellipse(crowd_surface, crowd_color, (50, 10, 80, 25))
        pygame.draw.ellipse(crowd_surface, crowd_color, (100, 5, 120, 35))
        
        # Draw crowd at multiple positions
        for i in range(5):
            x_pos = (i * 200 + self.crowd_offset) % (self.screen_width + 200) - 100
            surface.blit(crowd_surface, (x_pos, self.screen_height - 100))
    
    def _draw_logo(self, surface):
        """Draw the game logo with star animation."""
        # Draw "Pride of Code" text with outline
        logo_text = self.text_renderer.render_text(
            "PRIDE OF CODE", 
            style='title', 
            color=GOLD_EXCELLENCE, 
            outline=True
        )
        logo_rect = logo_text.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(logo_text, logo_rect)
        
        # Draw star animation
        self.star_timer += 1
        if self.star_timer >= 240:  # 4 seconds at 60 FPS
            self.star_visible = not self.star_visible
            self.star_timer = 0
            
            # Add sparkle effect when star appears
            if self.star_visible:
                sparkle = SparkleEffect(
                    logo_rect.centerx + 100, 
                    logo_rect.centery - 20
                )
                self.animation_manager.add_animation(sparkle)
        
        if self.star_visible:
            # Draw simple 8-bit star
            star_points = [
                (logo_rect.centerx + 100, logo_rect.centery - 25),  # Top
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Top-right
                (logo_rect.centerx + 110, logo_rect.centery - 25),  # Right
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Back to top-right
                (logo_rect.centerx + 110, logo_rect.centery - 15),  # Bottom-right
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Back to top-right
                (logo_rect.centerx + 100, logo_rect.centery - 15),  # Bottom
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Back to top-right
                (logo_rect.centerx + 95, logo_rect.centery - 15),   # Bottom-left
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Back to top-right
                (logo_rect.centerx + 90, logo_rect.centery - 25),   # Left
                (logo_rect.centerx + 105, logo_rect.centery - 20),  # Back to top-right
                (logo_rect.centerx + 95, logo_rect.centery - 20),   # Top-left
            ]
            
            pygame.draw.lines(surface, SILVER_STEEL, False, star_points, 2)
    
    def handle_event(self, event):
        """Handle pygame events."""
        for button in self.buttons:
            button.handle_event(event)
    
    def update(self, dt):
        """Update scene state."""
        # Update crowd animation
        self.crowd_offset += self.crowd_speed * dt
        
        # Update buttons
        for button in self.buttons:
            button.update(dt)
        
        # Update animations
        self.animation_manager.update(dt)
    
    def draw(self, surface):
        """Draw the main menu scene."""
        # Draw background
        self._draw_background(surface)
        
        # Draw logo
        self._draw_logo(surface)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Draw animations
        self.animation_manager.draw(surface)