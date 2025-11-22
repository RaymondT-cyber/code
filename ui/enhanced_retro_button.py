
"""Enhanced Retro-style UI buttons with pixel perfect aesthetic for Pride of Code.
Features improved styling, animations, and accessibility support.
"""

import pygame
import math
from typing import Optional, Callable
from config import COLOR_BLUE, COLOR_GOLD, COLOR_TEXT


class EnhancedRetroButton:
    """An enhanced retro-styled button with pixel art aesthetic and animations."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, color=None, text_color=None, 
                 on_click: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color or COLOR_BLUE
        self.text_color = text_color or COLOR_TEXT
        self.hover_color = COLOR_GOLD
        self.is_hovered = False
        self.is_pressed = False
        self.on_click = on_click
        
        # Animation properties
        self.hover_animation = 0.0
        self.press_animation = 0.0
        self.glow_animation = 0.0
        
        # Use pixel font for retro aesthetic
        try:
            self.font = pygame.font.Font(None, 24)  # Pixel font
        except:
            self.font = pygame.font.SysFont('arial', 20, bold=True)
            
        # Retro bowl styling properties
        self.pixel_size = 2  # For pixel art effects
        self.border_width = 3
        self.corner_radius = 6
        
        # Accessibility properties
        self.focused = False
        self.accessible_label = text
        
    def handle_event(self, event) -> bool:
        """Handle mouse and keyboard events. Returns True if button was clicked."""
        
        # Mouse events
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                self.press_animation = 1.0
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered:
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.is_pressed = False
            
        # Keyboard events for accessibility
        elif event.type == pygame.KEYDOWN:
            if self.focused and event.key == pygame.K_RETURN:
                self.is_pressed = True
                self.press_animation = 1.0
                
        elif event.type == pygame.KEYUP:
            if self.focused and event.key == pygame.K_RETURN and self.is_pressed:
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
                
        return False
        
    def update(self, dt: float):
        """Update animations."""
        # Hover animation
        if self.is_hovered:
            self.hover_animation = min(1.0, self.hover_animation + dt * 5)
        else:
            self.hover_animation = max(0.0, self.hover_animation - dt * 5)
            
        # Press animation
        if self.press_animation > 0:
            self.press_animation = max(0.0, self.press_animation - dt * 8)
            
        # Glow animation
        self.glow_animation += dt * 2
        
    def draw(self, surface: pygame.Surface):
        """Draw the button with enhanced retro styling."""
        
        # Calculate animation offsets
        hover_scale = 1.0 + (self.hover_animation * 0.05)
        press_offset = int(self.press_animation * 3)
        glow_intensity = abs(math.sin(self.glow_animation)) * self.hover_animation
        
        # Determine base color
        if self.is_pressed:
            base_color = tuple(max(0, c - 30) for c in self.color)
        elif self.is_hovered:
            base_color = self.hover_color
        else:
            base_color = self.color
            
        # Draw shadow with pixel style
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=self.corner_radius)
        
        # Draw main button with rounded corners effect
        button_rect = self.rect.copy()
        button_rect.y += press_offset
        button_rect.x += press_offset
        
        # Apply hover scale
        if hover_scale > 1.0:
            scaled_width = int(self.rect.width * hover_scale)
            scaled_height = int(self.rect.height * hover_scale)
            button_rect = pygame.Rect(
                self.rect.centerx - scaled_width // 2,
                self.rect.centery - scaled_height // 2 + press_offset,
                scaled_width,
                scaled_height
            )
        
        # Draw button background with retro bowl colors
        pygame.draw.rect(surface, base_color, button_rect, border_radius=self.corner_radius)
        
        # Draw pixel-style border
        pygame.draw.rect(surface, self.text_color, button_rect, self.border_width, border_radius=self.corner_radius)
        
        # Add inner highlight for depth
        highlight_rect = button_rect.inflate(-8, -8)
        pygame.draw.rect(surface, (255, 255, 255, 100), highlight_rect, 1, border_radius=self.corner_radius-2)
        
        # Add glow effect when hovered
        if glow_intensity > 0:
            glow_color = tuple(min(255, int(c + glow_intensity * 50)) for c in self.hover_color)
            glow_rect = button_rect.inflate(6, 6)
            pygame.draw.rect(surface, glow_color, glow_rect, 2, border_radius=self.corner_radius+3)
            
        # Draw retro bowl pixel art decorations
        self._draw_pixel_decorations(surface, button_rect)
        
        # Draw text with shadow
        text_shadow = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_shadow.get_rect(center=(button_rect.centerx + 1, button_rect.centery + 1))
        surface.blit(text_shadow, text_rect)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        surface.blit(text_surf, text_rect)
        
        # Draw focus indicator for keyboard navigation
        if self.focused:
            pygame.draw.rect(surface, COLOR_GOLD, button_rect, 3, border_radius=self.corner_radius)
            
    def _draw_pixel_decorations(self, surface: pygame.Surface, button_rect: pygame.Rect):
        """Draw retro bowl pixel art decorations on the button."""
        # Draw pixel dots in corners for retro effect
        if self.hover_animation > 0:
            dot_size = 3
            pulse = abs(math.sin(self.glow_animation * 3)) * self.hover_animation
            
            # Corner positions
            corners = [
                (button_rect.left + 10, button_rect.top + 10),
                (button_rect.right - 10, button_rect.top + 10),
                (button_rect.left + 10, button_rect.bottom - 10),
                (button_rect.right - 10, button_rect.bottom - 10)
            ]
            
            # Draw pulsing dots
            for corner in corners:
                dot_color = tuple(min(255, int(c + pulse * 100)) for c in self.hover_color)
                pygame.draw.rect(surface, dot_color,
                               (corner[0] - dot_size//2, corner[1] - dot_size//2,
                                dot_size, dot_size))
                                
            # Draw small pixel lines for extra retro effect
            line_length = int(10 + pulse * 5)
            line_color = tuple(min(255, int(c + pulse * 50)) for c in self.text_color)
            
            # Horizontal lines
            pygame.draw.line(surface, line_color,
                           (button_rect.left + 20, button_rect.top + 5),
                           (button_rect.left + 20 + line_length, button_rect.top + 5), 2)
            pygame.draw.line(surface, line_color,
                           (button_rect.right - 20 - line_length, button_rect.top + 5),
                           (button_rect.right - 20, button_rect.top + 5), 2)
                           
            # Vertical lines
            pygame.draw.line(surface, line_color,
                           (button_rect.left + 5, button_rect.top + 20),
                           (button_rect.left + 5, button_rect.top + 20 + line_length), 2)
            pygame.draw.line(surface, line_color,
                           (button_rect.left + 5, button_rect.bottom - 20 - line_length),
                           (button_rect.left + 5, button_rect.bottom - 20), 2)
            
    def set_text(self, text: str):
        """Update button text."""
        self.text = text
        self.accessible_label = text
        
    def set_focused(self, focused: bool):
        """Set keyboard focus state."""
        self.focused = focused
        
    def get_accessible_label(self) -> str:
        """Get the accessible label for screen readers."""
        return self.accessible_label


class AnimatedPixelButton(EnhancedRetroButton):
    """A button with pixel art animations."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, animation_type="pulse", **kwargs):
        super().__init__(x, y, width, height, text, **kwargs)
        self.animation_type = animation_type
        self.animation_time = 0.0
        
    def update(self, dt: float):
        """Update animations including pixel art effects."""
        super().update(dt)
        self.animation_time += dt
        
    def draw(self, surface: pygame.Surface):
        """Draw button with pixel art decorations."""
        super().draw(surface)
        
        # Add pixel art decorations based on animation type
        if self.animation_type == "pulse":
            self._draw_pulse_dots(surface)
        elif self.animation_type == "march":
            self._draw_march_dots(surface)
        elif self.animation_type == "sparkle":
            self._draw_sparkle_dots(surface)
            
    def _draw_pulse_dots(self, surface: pygame.Surface):
        """Draw pulsing pixel dots around the button."""
        if self.hover_animation > 0:
            pulse = abs(math.sin(self.animation_time * 3)) * self.hover_animation
            dot_size = int(2 + pulse * 2)
            
            # Corner dots
            corners = [
                (self.rect.left - 15, self.rect.top),
                (self.rect.right + 15, self.rect.top),
                (self.rect.left - 15, self.rect.bottom),
                (self.rect.right + 15, self.rect.bottom)
            ]
            
            for corner in corners:
                pygame.draw.rect(surface, COLOR_GOLD, 
                               (corner[0] - dot_size//2, corner[1] - dot_size//2, 
                                dot_size, dot_size))
                                
    def _draw_march_dots(self, surface: pygame.Surface):
        """Draw marching dots animation."""
        if self.hover_animation > 0:
            offset = (self.animation_time * 50) % 20
            
            for i in range(3):
                y_pos = self.rect.top - 20 + i * 10
                x_offset = (offset + i * 7) % 20 - 10
                
                pygame.draw.rect(surface, COLOR_GOLD,
                               (self.rect.centerx + x_offset - 3, y_pos, 6, 6))
                               
    def _draw_sparkle_dots(self, surface: pygame.Surface):
        """Draw sparkling pixel dots."""
        if self.hover_animation > 0:
            sparkle_count = 8
            for i in range(sparkle_count):
                angle = (self.animation_time * 2 + i * (2 * math.pi / sparkle_count)) % (2 * math.pi)
                distance = 25 + abs(math.sin(self.animation_time * 3 + i)) * 10
                x = self.rect.centerx + int(distance * math.cos(angle))
                y = self.rect.centery + int(distance * math.sin(angle))
                
                # Pulsing sparkle
                pulse = abs(math.sin(self.animation_time * 5 + i))
                size = int(2 + pulse * 3)
                
                pygame.draw.rect(surface, COLOR_GOLD, (x - size//2, y - size//2, size, size))
