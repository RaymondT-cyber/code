"""
Pride of Code UI Components
===========================

Reusable UI components that follow the visual identity style guide.

Style Guide Reference:
Section 4. Micro-Detail Visual Rules
Section 5. Screen-Specific Visual Design
"""

import pygame
import math
from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, NEON_COMPETENCE_CYAN, GOLD_EXCELLENCE,
    PRECISION_MAGENTA, ERROR_RED, STADIUM_TURF_GREEN
)


class UIComponent:
    """Base class for all UI components."""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
    
    def draw(self, surface):
        """Draw the component on the given surface."""
        pass
    
    def handle_event(self, event):
        """Handle pygame events."""
        pass
    
    def update(self, dt):
        """Update component state."""
        pass


class RetroButton(UIComponent):
    """
    Styled button following the visual identity guidelines.
    
    Style Guide Reference:
    Section 4.2 Button Design
    """
    
    def __init__(self, x, y, width, height, text="", font_size=18):
        super().__init__(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.state = "normal"  # normal, hover, pressed
        self.click_callback = None
        self.font = pygame.font.Font(None, font_size)  # Will be replaced with pixel font
        
        # Animation properties
        self.pressed_offset = 0
        self.glow_alpha = 0
        
    def set_click_callback(self, callback):
        """Set the function to call when button is clicked."""
        self.click_callback = callback
    
    def draw(self, surface):
        """Draw the button with appropriate styling based on state."""
        if not self.visible:
            return
            
        # Calculate button position with pressed offset
        draw_rect = self.rect.copy()
        draw_rect.y += self.pressed_offset
        
        # Draw button background based on state
        if self.state == "pressed":
            button_color = ColorPalette.adjust_brightness(DEEP_SIGNAL_BLUE, 0.9)
        elif self.state == "hover":
            button_color = DEEP_SIGNAL_BLUE
        else:
            button_color = DEEP_SIGNAL_BLUE
            
        # Draw main button
        pygame.draw.rect(surface, button_color, draw_rect, border_radius=4)
        
        # Draw border
        pygame.draw.rect(surface, SILVER_STEEL, draw_rect, 2, border_radius=4)
        
        # Draw inner highlight for normal/hover states
        if self.state != "pressed":
            highlight_rect = pygame.Rect(
                draw_rect.x + 1, 
                draw_rect.y + 1, 
                draw_rect.width - 2, 
                2
            )
            pygame.draw.rect(surface, RETRO_PIXEL_AMBER, highlight_rect)
        
        # Draw glow effect for hover state
        if self.state == "hover" and self.glow_alpha > 0:
            glow_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            glow_color = pygame.Color(NEON_COMPETENCE_CYAN.r, NEON_COMPETENCE_CYAN.g, 
                                    NEON_COMPETENCE_CYAN.b, int(self.glow_alpha * 255 * 0.15))
            pygame.draw.rect(glow_surf, glow_color, 
                           pygame.Rect(0, 0, draw_rect.width, draw_rect.height), 
                           border_radius=4)
            surface.blit(glow_surf, draw_rect)
        
        # Draw text
        if self.text:
            text_surf = self.font.render(self.text, True, SILVER_STEEL)
            text_rect = text_surf.get_rect(center=draw_rect.center)
            surface.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        """Handle mouse events for button interaction."""
        if not self.enabled or not self.visible:
            return
            
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.state != "pressed":
                    self.state = "hover"
                    self.glow_alpha = 1.0
            else:
                self.state = "normal"
                self.glow_alpha = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                self.state = "pressed"
                self.pressed_offset = 1
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.state == "pressed" and self.rect.collidepoint(event.pos):
                    if self.click_callback:
                        self.click_callback()
                self.state = "normal" if self.rect.collidepoint(event.pos) else "normal"
                self.pressed_offset = 0
    
    def update(self, dt):
        """Update button animations."""
        if self.state == "hover" and self.glow_alpha > 0:
            self.glow_alpha = max(0, self.glow_alpha - dt * 2)  # Fade out glow


class RetroPanel(UIComponent):
    """
    Styled panel following the visual identity guidelines.
    
    Style Guide Reference:
    Section 5 Screen-Specific Visual Design
    """
    
    def __init__(self, x, y, width, height, border_color=SILVER_STEEL, 
                 background_color=DARK_GRAPHITE_BLACK, border_width=1):
        super().__init__(x, y, width, height)
        self.border_color = border_color
        self.background_color = background_color
        self.border_width = border_width
    
    def draw(self, surface):
        """Draw the panel with appropriate styling."""
        if not self.visible:
            return
            
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Draw border
        for i in range(self.border_width):
            border_rect = pygame.Rect(
                self.rect.x + i,
                self.rect.y + i,
                self.rect.width - 2 * i,
                self.rect.height - 2 * i
            )
            pygame.draw.rect(surface, self.border_color, border_rect, 1)


class ScoreBar(UIComponent):
    """
    Animated score bar for displaying performance metrics.
    
    Style Guide Reference:
    Section 5.5 Competition Scene - HUD
    """
    
    def __init__(self, x, y, width, height, color, label="", max_value=100):
        super().__init__(x, y, width, height)
        self.color = color
        self.label = label
        self.max_value = max_value
        self.current_value = 0
        self.target_value = 0
        self.animation_speed = 50  # units per second
        
        # Font for label
        self.font = pygame.font.Font(None, 16)
    
    def set_value(self, value):
        """Set the target value for the bar."""
        self.target_value = max(0, min(self.max_value, value))
    
    def draw(self, surface):
        """Draw the score bar with styling."""
        if not self.visible:
            return
            
        # Draw background
        pygame.draw.rect(surface, DARK_GRAPHITE_BLACK, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, SILVER_STEEL, self.rect, 1)
        
        # Draw filled portion
        if self.max_value > 0:
            fill_width = int((self.current_value / self.max_value) * (self.rect.width - 2))
            if fill_width > 0:
                fill_rect = pygame.Rect(
                    self.rect.x + 1,
                    self.rect.y + 1,
                    fill_width,
                    self.rect.height - 2
                )
                pygame.draw.rect(surface, self.color, fill_rect)
                
                # Draw inner highlight
                highlight_rect = pygame.Rect(
                    self.rect.x + 1,
                    self.rect.y + 1,
                    fill_width,
                    2
                )
                highlight_color = ColorPalette.adjust_brightness(self.color, 1.3)
                pygame.draw.rect(surface, highlight_color, highlight_rect)
        
        # Draw label
        if self.label:
            label_surf = self.font.render(self.label, True, SILVER_STEEL)
            surface.blit(label_surf, (self.rect.x, self.rect.y - 20))
    
    def update(self, dt):
        """Update the bar animation."""
        # Smoothly animate to target value
        difference = self.target_value - self.current_value
        if abs(difference) > 0.1:
            step = self.animation_speed * dt
            if difference > 0:
                self.current_value = min(self.target_value, self.current_value + step)
            else:
                self.current_value = max(self.target_value, self.current_value - step)
        else:
            self.current_value = self.target_value


class TextRenderer:
    """
    Text rendering system with pixel-style styling.
    
    Style Guide Reference:
    Section 3. Typography Specification
    """
    
    def __init__(self):
        # In a real implementation, you would load pixel fonts here
        self.fonts = {
            'small': pygame.font.Font(None, 16),
            'medium': pygame.font.Font(None, 18),
            'large': pygame.font.Font(None, 22),
            'title': pygame.font.Font(None, 32)
        }
    
    def render_text(self, text, style='medium', color=SILVER_STEEL, outline=False):
        """
        Render text with optional outline.
        
        Args:
            text: String to render
            style: Font style ('small', 'medium', 'large', 'title')
            color: Text color
            outline: Whether to add a 1px outline
            
        Returns:
            pygame.Surface with rendered text
        """
        font = self.fonts.get(style, self.fonts['medium'])
        
        if outline:
            # Create text with outline by rendering multiple times with offset
            outline_surface = pygame.Surface(
                (font.size(text)[0] + 2, font.size(text)[1] + 2), 
                pygame.SRCALPHA
            )
            
            # Draw outline in background color
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        outline_text = font.render(text, True, SILVER_STEEL)
                        outline_surface.blit(outline_text, (dx + 1, dy + 1))
            
            # Draw main text in center
            main_text = font.render(text, True, color)
            outline_surface.blit(main_text, (1, 1))
            return outline_surface
        else:
            return font.render(text, True, color)


# Convenience class for accessing color palette methods
class ColorPalette:
    """Helper class for color manipulation."""
    
    @staticmethod
    def adjust_brightness(color, factor):
        """Adjust the brightness of a color."""
        r = min(255, max(0, int(color.r * factor)))
        g = min(255, max(0, int(color.g * factor)))
        b = min(255, max(0, int(color.b * factor)))
        return pygame.Color(r, g, b, color.a)
    
    @staticmethod
    def with_alpha(color, alpha):
        """Create a copy of a color with specified alpha."""
        return pygame.Color(color.r, color.g, color.b, alpha)