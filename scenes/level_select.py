"""
Pride of Code Level Select Screen
=================================

Implementation of the level select screen following the visual identity style guide.

Style Guide Reference:
Section 5.2 Level Select / Week Planner
"""

import pygame
from core.colors import (
    DARK_GRAPHITE_BLACK, RETRO_PIXEL_AMBER, DEEP_SIGNAL_BLUE,
    SILVER_STEEL, STADIUM_TURF_GREEN, PRECISION_MAGENTA,
    GOLD_EXCELLENCE
)
from ui.components import UIComponent, RetroPanel, TextRenderer


class LevelSelectScene:
    """
    Level select screen implementation.
    
    Style Guide Reference:
    Section 5.2 Level Select / Week Planner
    """
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
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


# Define RetroButton here to avoid circular imports
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
        from core.colors import DEEP_SIGNAL_BLUE, SILVER_STEEL, RETRO_PIXEL_AMBER, NEON_COMPETENCE_CYAN
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
            from core.colors import SILVER_STEEL
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