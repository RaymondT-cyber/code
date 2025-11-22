"""
Pride of Code - Complete Game Implementation
============================================

This is the main game file that consolidates all visual components and game systems.
"""

import pygame
import time
import math
import random
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# -------------------------------
# Color System
# -------------------------------
import pygame


class ColorPalette:
    """Complete color palette implementation for Pride of Code."""
    
    # Primary Colors
    DARK_GRAPHITE_BLACK = pygame.Color(26, 28, 30)  # #1A1C1E
    RETRO_PIXEL_AMBER = pygame.Color(242, 169, 0)    # #F2A900
    DEEP_SIGNAL_BLUE = pygame.Color(33, 70, 199)     # #2146C7
    
    # Secondary Colors
    SILVER_STEEL = pygame.Color(197, 202, 211)       # #C5CAD3
    STADIUM_TURF_GREEN = pygame.Color(59, 142, 46)   # #3B8E2E
    ERROR_RED = pygame.Color(194, 55, 55)            # #C23737
    
    # Highlight Colors
    NEON_COMPETENCE_CYAN = pygame.Color(67, 224, 236)  # #43E0EC
    PRECISION_MAGENTA = pygame.Color(235, 63, 190)     # #EB3FBE
    GOLD_EXCELLENCE = pygame.Color(255, 201, 71)       # #FFC947
    
    # Additional UI Colors
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    SEMI_TRANSPARENT_BLACK = pygame.Color(0, 0, 0, 178)  # 70% opacity
    DARKER_GRAPHITE = pygame.Color(15, 16, 17)           # #0F1011
    
    # Color name to value mapping for easy access
    COLOR_MAP = {
        'dark_graphite_black': DARK_GRAPHITE_BLACK,
        'retro_pixel_amber': RETRO_PIXEL_AMBER,
        'deep_signal_blue': DEEP_SIGNAL_BLUE,
        'silver_steel': SILVER_STEEL,
        'stadium_turf_green': STADIUM_TURF_GREEN,
        'error_red': ERROR_RED,
        'neon_competence_cyan': NEON_COMPETENCE_CYAN,
        'precision_magenta': PRECISION_MAGENTA,
        'gold_excellence': GOLD_EXCELLENCE,
        'transparent': TRANSPARENT,
        'semi_transparent_black': SEMI_TRANSPARENT_BLACK,
        'darker_graphite': DARKER_GRAPHITE
    }
    
    @classmethod
    def get_color(cls, name):
        """Get a color by its name."""
        return cls.COLOR_MAP.get(name.lower(), cls.DARK_GRAPHITE_BLACK)
    
    @classmethod
    def adjust_brightness(cls, color, factor):
        """
        Adjust the brightness of a color.
        
        Args:
            color: pygame.Color to adjust
            factor: float between 0.0 (black) and 2.0 (double brightness)
            
        Returns:
            pygame.Color with adjusted brightness
        """
        r = min(255, max(0, int(color.r * factor)))
        g = min(255, max(0, int(color.g * factor)))
        b = min(255, max(0, int(color.b * factor)))
        return pygame.Color(r, g, b, color.a)
    
    @classmethod
    def with_alpha(cls, color, alpha):
        """
        Create a copy of a color with specified alpha.
        
        Args:
            color: pygame.Color to modify
            alpha: int between 0 (transparent) and 255 (opaque)
            
        Returns:
            pygame.Color with specified alpha
        """
        return pygame.Color(color.r, color.g, color.b, alpha)


# Convenience constants for direct access
DARK_GRAPHITE_BLACK = ColorPalette.DARK_GRAPHITE_BLACK
RETRO_PIXEL_AMBER = ColorPalette.RETRO_PIXEL_AMBER
DEEP_SIGNAL_BLUE = ColorPalette.DEEP_SIGNAL_BLUE
SILVER_STEEL = ColorPalette.SILVER_STEEL
STADIUM_TURF_GREEN = ColorPalette.STADIUM_TURF_GREEN
ERROR_RED = ColorPalette.ERROR_RED
NEON_COMPETENCE_CYAN = ColorPalette.NEON_COMPETENCE_CYAN
PRECISION_MAGENTA = ColorPalette.PRECISION_MAGENTA
GOLD_EXCELLENCE = ColorPalette.GOLD_EXCELLENCE
TRANSPARENT = ColorPalette.TRANSPARENT
SEMI_TRANSPARENT_BLACK = ColorPalette.SEMI_TRANSPARENT_BLACK
DARKER_GRAPHITE = ColorPalette.DARKER_GRAPHITE


# -------------------------------
# UI Components
# -------------------------------
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


# -------------------------------
# Animation System
# -------------------------------
class AnimationManager:
    """Central manager for all animations in the game."""
    
    def __init__(self):
        self.animations = []
    
    def add_animation(self, animation):
        """Add an animation to be managed."""
        self.animations.append(animation)
    
    def remove_animation(self, animation):
        """Remove an animation from management."""
        if animation in self.animations:
            self.animations.remove(animation)
    
    def update(self, dt):
        """Update all managed animations."""
        for animation in self.animations[:]:  # Copy list to allow removal during iteration
            animation.update(dt)
            if animation.is_finished():
                self.animations.remove(animation)
    
    def draw(self, surface):
        """Draw all managed animations."""
        for animation in self.animations:
            animation.draw(surface)


class Animation:
    """Base class for all animations."""
    
    def __init__(self, duration):
        self.duration = duration
        self.time_elapsed = 0
        self.finished = False
    
    def update(self, dt):
        """Update animation state."""
        self.time_elapsed += dt
        if self.time_elapsed >= self.duration:
            self.finished = True
            self.on_finish()
    
    def is_finished(self):
        """Check if animation has finished."""
        return self.finished
    
    def draw(self, surface):
        """Draw the animation."""
        pass
    
    def on_finish(self):
        """Called when animation finishes."""
        pass


class ButtonHoverGlow(Animation):
    """
    Button hover shimmer effect.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Button hover shimmer
    """
    
    def __init__(self, button_rect, duration=0.5):
        super().__init__(duration)
        self.button_rect = button_rect
        self.max_alpha = 38  # 15% of 255
    
    def update(self, dt):
        super().update(dt)
    
    def draw(self, surface):
        if not self.is_finished():
            # Calculate current alpha (pulse effect)
            progress = self.time_elapsed / self.duration
            alpha = self.max_alpha * (0.5 + 0.5 * math.sin(progress * math.pi * 4))
            
            # Create glow surface
            glow_surf = pygame.Surface((self.button_rect.width, self.button_rect.height), pygame.SRCALPHA)
            glow_color = (67, 224, 236, int(alpha))  # NEON_COMPETENCE_CYAN with alpha
            pygame.draw.rect(glow_surf, glow_color, 
                           pygame.Rect(0, 0, self.button_rect.width, self.button_rect.height), 
                           border_radius=4)
            surface.blit(glow_surf, self.button_rect)


class ScoreBarFill(Animation):
    """
    Score bar fill increment animation.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Score bar fill increments with 1px steps
    """
    
    def __init__(self, bar_rect, start_value, end_value, duration=0.3):
        super().__init__(duration)
        self.bar_rect = bar_rect
        self.start_value = start_value
        self.end_value = end_value
        self.current_value = start_value
    
    def update(self, dt):
        super().update(dt)
        if not self.is_finished():
            progress = self.time_elapsed / self.duration
            self.current_value = self.start_value + (self.end_value - self.start_value) * progress
    
    def draw(self, surface):
        # This animation doesn't draw directly, it updates the bar value
        pass
    
    def get_current_value(self):
        return self.current_value


class SparkleEffect(Animation):
    """
    Tiny pixel sparkles around high scores.
    
    Style Guide Reference:
    Section 6. Micro-Animations - Tiny pixel sparkles around high scores
    """
    
    def __init__(self, x, y, duration=1.0, count=5):
        super().__init__(duration)
        self.x = x
        self.y = y
        self.particles = []
        
        # Create particles
        for _ in range(count):
            particle = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'size': random.randint(1, 2),
                'speed_x': random.uniform(-20, 20),
                'speed_y': random.uniform(-20, 20),
                'alpha': 255
            }
            self.particles.append(particle)
    
    def update(self, dt):
        super().update(dt)
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['speed_x'] * dt
            particle['y'] += particle['speed_y'] * dt
            particle['alpha'] = max(0, particle['alpha'] - 200 * dt)
    
    def draw(self, surface):
        if not self.is_finished():
            for particle in self.particles:
                if particle['alpha'] > 0:
                    color = (255, 255, 255, int(particle['alpha']))
                    s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                    s.fill(color)
                    surface.blit(s, (particle['x'], particle['y']))


class PixelDissolve(Animation):
    """
    Pixel dissolve transition effect.
    
    Style Guide Reference:
    Section 6. Global Animation Rules - Transitions are slide, fade, or pixel dissolve (3–5 frames)
    """
    
    def __init__(self, surface, rect, duration=0.5):
        super().__init__(duration)
        self.surface = surface
        self.rect = rect
        self.pixel_size = 3  # Size of dissolve blocks
    
    def draw(self, surface):
        if not self.is_finished():
            # Create a copy of the surface
            temp_surface = self.surface.copy()
            
            # Calculate dissolve progress
            progress = self.time_elapsed / self.duration
            
            # Draw grid of pixels that disappear over time
            for y in range(0, self.rect.height, self.pixel_size):
                for x in range(0, self.rect.width, self.pixel_size):
                    # Random threshold determines when this pixel disappears
                    threshold = random.random() * 1.2
                    if progress > threshold:
                        pygame.draw.rect(temp_surface, (0, 0, 0), 
                                       pygame.Rect(self.rect.x + x, self.rect.y + y, 
                                                 self.pixel_size, self.pixel_size))
            
            surface.blit(temp_surface, self.rect)


# -------------------------------
# Game Scenes
# -------------------------------
class Scene:
    """Base class for all game scenes."""
    
    def __init__(self, game):
        self.game = game
    
    def handle_event(self, event):
        """Handle pygame events."""
        pass
    
    def update(self, dt):
        """Update scene state."""
        pass
    
    def draw(self, surface):
        """Draw the scene."""
        pass


class MainMenuScene(Scene):
    """
    Main menu screen implementation.
    
    Style Guide Reference:
    Section 5.1 Main Menu Screen
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.screen_width = 1024
        self.screen_height = 768
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
        pygame.quit()
        sys.exit()
    
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


class CodeEditorScene(Scene):
    """
    Code editor screen implementation.
    
    Style Guide Reference:
    Section 5.4 Code Editor Screen
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.screen_width = 1024
        self.screen_height = 768
        self.text_renderer = TextRenderer()
        
        # Editor state
        self.code_lines = [
            "def marching_band():",
            "    # Initialize band members",
            "    members = []",
            "    for i in range(8):",
            "        members.append(BandMember(i))",
            "    ",
            "    # Execute formation",
            "    execute_formation(members)",
            "    ",
            "    return 'Performance complete'"
        ]
        self.cursor_line = 0
        self.cursor_pos = 0
        self.scroll_offset = 0
        
        # Console output
        self.console_lines = [
            "Pride of Code v1.0",
            "Ready for performance!",
            ">>> marching_band()",
            "Performance complete"
        ]
        
        # Create UI panels
        self._create_panels()
        
        # Back button
        self.back_button = RetroButton(
            20, 20, 100, 40, "BACK"
        )
        self.back_button.set_click_callback(self._on_back_clicked)
    
    def _create_panels(self):
        """Create the editor and console panels."""
        # Editor panel (top 70% of screen)
        editor_height = int(self.screen_height * 0.7)
        self.editor_panel = RetroPanel(
            10, 10, 
            self.screen_width - 20, 
            editor_height - 20,
            border_color=SILVER_STEEL,
            background_color=DARK_GRAPHITE_BLACK,
            border_width=1
        )
        
        # Console panel (bottom 30% of screen)
        console_height = int(self.screen_height * 0.3)
        self.console_panel = RetroPanel(
            10, editor_height + 10,
            self.screen_width - 20,
            console_height - 20,
            border_color=SILVER_STEEL,
            background_color=DARKER_GRAPHITE,
            border_width=1
        )
    
    def _on_back_clicked(self):
        """Handle back button click."""
        print("Back to main menu")
        # In a real implementation, this would transition to the main menu
    
    def _draw_editor_background(self, surface):
        """Draw the editor background with vignette and scanlines."""
        panel_rect = self.editor_panel.rect
        
        # Draw vignette effect (subtle darkening at edges)
        vignette_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        for y in range(panel_rect.height):
            for x in range(panel_rect.width):
                # Calculate distance from center
                center_x, center_y = panel_rect.width // 2, panel_rect.height // 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = (center_x ** 2 + center_y ** 2) ** 0.5
                
                # Calculate vignette intensity (8-10%)
                intensity = 1.0 - (distance / max_distance) * 0.09
                vignette_surf.set_at((x, y), (0, 0, 0, int(255 * (1 - intensity))))
        
        surface.blit(vignette_surf, panel_rect)
        
        # Draw subtle scanlines
        for y in range(0, panel_rect.height, 2):
            scanline = pygame.Surface((panel_rect.width, 1), pygame.SRCALPHA)
            scanline.fill((0, 0, 0, int(255 * 0.02)))  # 2% opacity
            surface.blit(scanline, (panel_rect.x, panel_rect.y + y))
    
    def _draw_code(self, surface):
        """Draw the code with syntax highlighting."""
        panel_rect = self.editor_panel.rect
        
        # Font for code
        font = self.text_renderer.fonts['large']
        line_height = font.get_height()
        
        # Draw each line of code
        for i, line in enumerate(self.code_lines):
            y_pos = panel_rect.y + 20 + (i - self.scroll_offset) * line_height
            
            # Skip lines outside the visible area
            if y_pos < panel_rect.y - line_height or y_pos > panel_rect.y + panel_rect.height:
                continue
            
            # Highlight current line
            if i == self.cursor_line:
                highlight_rect = pygame.Rect(
                    panel_rect.x + 5,
                    y_pos,
                    panel_rect.width - 10,
                    line_height
                )
                pygame.draw.rect(surface, (30, 30, 40), highlight_rect)
            
            # Apply syntax highlighting
            self._draw_syntax_highlighted_line(surface, line, panel_rect.x + 10, y_pos)
            
            # Draw line numbers
            line_num = str(i + 1)
            line_num_surf = font.render(line_num, True, SILVER_STEEL)
            line_num_rect = line_num_surf.get_rect()
            line_num_rect.right = panel_rect.x - 5
            line_num_rect.y = y_pos
            surface.blit(line_num_surf, line_num_rect)
    
    def _draw_syntax_highlighted_line(self, surface, line, x, y):
        """Draw a line of code with syntax highlighting."""
        font = self.text_renderer.fonts['large']
        
        # Simple syntax highlighting based on keywords
        keywords = ['def', 'for', 'if', 'else', 'return', 'in', 'range']
        functions = ['marching_band', 'BandMember', 'execute_formation']
        
        # Split line into tokens
        tokens = line.split(' ')
        current_x = x
        
        for token in tokens:
            # Determine token color
            color = SILVER_STEEL  # Default color
            
            # Check for keywords
            clean_token = token.strip('():,')
            if clean_token in keywords:
                color = DEEP_SIGNAL_BLUE
            elif clean_token in functions:
                color = PRECISION_MAGENTA
            elif clean_token.startswith('#'):
                color = pygame.Color(SILVER_STEEL.r, SILVER_STEEL.g, SILVER_STEEL.b, int(255 * 0.6))
            elif clean_token.startswith('"') or clean_token.startswith("'") or \
                 (token.startswith('"') and token.endswith('"')) or \
                 (token.startswith("'") and token.endswith("'")):
                color = RETRO_PIXEL_AMBER
            elif clean_token == 'True' or clean_token == 'False' or clean_token.isdigit():
                color = RETRO_PIXEL_AMBER
            
            # Render token
            token_surf = font.render(token + ' ', True, color)
            surface.blit(token_surf, (current_x, y))
            current_x += token_surf.get_width()
    
    def _draw_console(self, surface):
        """Draw the console output."""
        panel_rect = self.console_panel.rect
        
        # Font for console
        font = self.text_renderer.fonts['medium']
        line_height = font.get_height()
        
        # Draw each line of console output
        for i, line in enumerate(self.console_lines):
            y_pos = panel_rect.y + 10 + i * line_height
            
            # Skip lines outside the visible area
            if y_pos < panel_rect.y or y_pos > panel_rect.y + panel_rect.height - line_height:
                continue
            
            # Determine line color
            color = SILVER_STEEL
            if "Error" in line or "error" in line:
                color = ERROR_RED
            elif "complete" in line.lower():
                color = STADIUM_TURF_GREEN
            
            # Render line
            line_surf = font.render(line, True, color)
            surface.blit(line_surf, (panel_rect.x + 10, y_pos))
    
    def _draw_gutter_markers(self, surface):
        """Draw error markers in the gutter."""
        panel_rect = self.editor_panel.rect
        font = self.text_renderer.fonts['large']
        line_height = font.get_height()
        
        # Draw error marker on line 7 (0-indexed)
        error_line = 7
        y_pos = panel_rect.y + 20 + (error_line - self.scroll_offset) * line_height
        
        if panel_rect.y <= y_pos <= panel_rect.y + panel_rect.height - line_height:
            # Draw error underline in the code
            error_text = self.code_lines[error_line]
            text_width = font.size(error_text)[0]
            pygame.draw.line(
                surface,
                ERROR_RED,
                (panel_rect.x + 10, y_pos + line_height - 2),
                (panel_rect.x + 10 + text_width, y_pos + line_height - 2),
                2
            )
            
            # Draw error icon in gutter
            error_icon = font.render("!", True, RETRO_PIXEL_AMBER)
            surface.blit(error_icon, (panel_rect.x - 15, y_pos))
    
    def handle_event(self, event):
        """Handle pygame events."""
        self.editor_panel.handle_event(event)
        self.console_panel.handle_event(event)
        self.back_button.handle_event(event)
        
        # Handle keyboard input for code editing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.cursor_line = max(0, self.cursor_line - 1)
            elif event.key == pygame.K_DOWN:
                self.cursor_line = min(len(self.code_lines) - 1, self.cursor_line + 1)
            elif event.key == pygame.K_RETURN:
                # Add new line
                self.code_lines.insert(self.cursor_line + 1, "")
                self.cursor_line += 1
                self.cursor_pos = 0
    
    def update(self, dt):
        """Update scene state."""
        self.editor_panel.update(dt)
        self.console_panel.update(dt)
        self.back_button.update(dt)
    
    def draw(self, surface):
        """Draw the code editor scene."""
        # Draw panels
        self.editor_panel.draw(surface)
        self.console_panel.draw(surface)
        self.back_button.draw(surface)
        
        # Draw editor background effects
        self._draw_editor_background(surface)
        
        # Draw code
        self._draw_code(surface)
        
        # Draw console output
        self._draw_console(surface)
        
        # Draw gutter markers
        self._draw_gutter_markers(surface)


class LevelSelectScene(Scene):
    """
    Level select screen implementation.
    
    Style Guide Reference:
    Section 5.2 Level Select / Week Planner
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.screen_width = 1024
        self.screen_height = 768
        self.text_renderer = TextRenderer()
        
        # Level grid properties
        self.tile_width = 120
        self.tile_height = 80
        self.columns = 2
        self.rows = 8
        self.tiles = []
        
        # Create level tiles
        self._create_level_tiles()
        
        # Back button
        self.back_button = RetroButton(
            20, 20, 100, 40, "BACK"
        )
        self.back_button.set_click_callback(self._on_back_clicked)
    
    def _create_level_tiles(self):
        """Create the level selection tiles."""
        # Calculate grid position (centered)
        grid_width = self.columns * self.tile_width + (self.columns - 1) * 20
        grid_height = self.rows * self.tile_height + (self.rows - 1) * 20
        start_x = (self.screen_width - grid_width) // 2
        start_y = (self.screen_height - grid_height) // 2 + 30
        
        # Create 16 tiles (2 columns x 8 rows)
        for row in range(self.rows):
            for col in range(self.columns):
                index = row * self.columns + col
                x = start_x + col * (self.tile_width + 20)
                y = start_y + row * (self.tile_height + 20)
                
                tile = LevelTile(x, y, self.tile_width, self.tile_height, index + 1)
                self.tiles.append(tile)
    
    def _on_back_clicked(self):
        """Handle back button click."""
        print("Back to main menu")
        # In a real implementation, this would transition to the main menu
    
    def handle_event(self, event):
        """Handle pygame events."""
        self.back_button.handle_event(event)
        
        # Handle tile clicks
        for tile in self.tiles:
            tile.handle_event(event)
    
    def update(self, dt):
        """Update scene state."""
        self.back_button.update(dt)
        
        # Update tiles
        for tile in self.tiles:
            tile.update(dt)
    
    def draw(self, surface):
        """Draw the level select scene."""
        # Draw title
        title_font = self.text_renderer.fonts['title']
        title = title_font.render("WEEK SELECT", True, GOLD_EXCELLENCE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title, title_rect)
        
        # Draw back button
        self.back_button.draw(surface)
        
        # Draw level tiles
        for tile in self.tiles:
            tile.draw(surface)


class LevelTile(UIComponent):
    """
    Individual level tile for the level select grid.
    
    Style Guide Reference:
    Section 5.2 Level Select / Week Planner - Tile Design
    """
    
    def __init__(self, x, y, width, height, week_number):
        super().__init__(x, y, width, height)
        self.week_number = week_number
        self.is_locked = week_number > 3  # Lock weeks beyond 3 for demo
        self.is_competition = week_number % 3 == 0  # Every 3rd week is competition
        self.hovered = False
        
        # Animation properties
        self.confetti_particles = []
        self.confetti_timer = 0
    
    def handle_event(self, event):
        """Handle mouse events for the tile."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                if not self.is_locked:
                    print(f"Selected Week {self.week_number}")
                    # In a real implementation, this would transition to the level
    
    def update(self, dt):
        """Update tile animations."""
        # Update confetti for competition weeks
        if self.is_competition and not self.is_locked:
            self.confetti_timer += dt
            if self.confetti_timer >= 0.2:  # Add particle every 0.2 seconds
                self.confetti_timer = 0
                if len(self.confetti_particles) < 20:  # Limit particles
                    particle = {
                        'x': self.rect.x + pygame.time.get_ticks() % self.rect.width,
                        'y': self.rect.y + pygame.time.get_ticks() % self.rect.height,
                        'color': [GOLD_EXCELLENCE, PRECISION_MAGENTA, STADIUM_TURF_GREEN][pygame.time.get_ticks() % 3],
                        'size': pygame.time.get_ticks() % 3 + 1,
                        'lifetime': 1.0
                    }
                    self.confetti_particles.append(particle)
            
            # Update particles
            for particle in self.confetti_particles[:]:
                particle['lifetime'] -= dt
                if particle['lifetime'] <= 0:
                    self.confetti_particles.remove(particle)
    
    def draw(self, surface):
        """Draw the level tile."""
        # Determine tile colors based on type
        if self.is_locked:
            background_color = pygame.Color(0, 0, 0, int(255 * 0.5))  # Semi-transparent black
            border_color = SILVER_STEEL
        elif self.is_competition:
            background_color = DEEP_SIGNAL_BLUE
            border_color = GOLD_EXCELLENCE
        else:
            # Dimmed Stadium Turf Green (70%)
            background_color = pygame.Color(
                int(STADIUM_TURF_GREEN.r * 0.7),
                int(STADIUM_TURF_GREEN.g * 0.7),
                int(STADIUM_TURF_GREEN.b * 0.7)
            )
            border_color = SILVER_STEEL
        
        # Draw tile background
        pygame.draw.rect(surface, background_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Draw week number badge
        badge_radius = 15
        badge_center = (self.rect.centerx, self.rect.y + 20)
        pygame.draw.circle(surface, GOLD_EXCELLENCE, badge_center, badge_radius)
        pygame.draw.circle(surface, SILVER_STEEL, badge_center, badge_radius, 2)
        
        # Draw week number
        font = pygame.font.Font(None, 24)
        week_text = font.render(str(self.week_number), True, DARK_GRAPHITE_BLACK)
        week_rect = week_text.get_rect(center=badge_center)
        surface.blit(week_text, week_rect)
        
        # Draw lock icon for locked weeks
        if self.is_locked:
            lock_font = pygame.font.Font(None, 32)
            lock_text = lock_font.render("🔒", True, PRECISION_MAGENTA)
            lock_rect = lock_text.get_rect(center=self.rect.center)
            surface.blit(lock_text, lock_rect)
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(255 * 0.5)))  # 50% transparent black
            surface.blit(overlay, self.rect)
        
        # Draw hover effect
        if self.hovered and not self.is_locked:
            highlight_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            highlight_color = pygame.Color(67, 224, 236, int(255 * 0.2))  # NEON_COMPETENCE_CYAN with 20% alpha
            pygame.draw.rect(highlight_surf, highlight_color, 
                           pygame.Rect(0, 0, self.rect.width, self.rect.height), 
                           border_radius=2)
            surface.blit(highlight_surf, self.rect)
        
        # Draw confetti for competition weeks
        if self.is_competition and not self.is_locked:
            for particle in self.confetti_particles:
                s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
                s.fill(particle['color'])
                surface.blit(s, (particle['x'], particle['y']))


# -------------------------------
# Game Engine
# -------------------------------
class PrideOfCodeGame:
    """Main game class that manages scenes and game loop."""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = 1024
        self.WINDOW_HEIGHT = 768
        self.GAME_TITLE = "Pride of Code"
        
        pygame.display.set_caption(self.GAME_TITLE)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        # Time management
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        
        # Game state
        self.current_scene = None
        self.scenes = {}
        
        # Initialize scenes
        self._init_scenes()
        
        # Start with main menu
        self.switch_scene("main_menu")
    
    def _init_scenes(self):
        """Initialize all game scenes."""
        self.scenes["main_menu"] = MainMenuScene(self)
        self.scenes["code_editor"] = CodeEditorScene(self)
        self.scenes["level_select"] = LevelSelectScene(self)
    
    def switch_scene(self, scene_name):
        """Switch to a different scene."""
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
        else:
            print(f"Scene '{scene_name}' not found!")
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Delta-time calculation
            now = time.time()
            dt = now - self.last_time
            self.last_time = now
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if self.current_scene:
                        self.current_scene.handle_event(event)
            
            # Update
            if self.current_scene:
                self.current_scene.update(dt)
            
            # Draw
            self.screen.fill(DARK_GRAPHITE_BLACK)
            if self.current_scene:
                self.current_scene.draw(self.screen)
            pygame.display.flip()
            
            # Framerate cap
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


# -------------------------------
# Main Entry Point
# -------------------------------
if __name__ == "__main__":
    game = PrideOfCodeGame()
    game.run()