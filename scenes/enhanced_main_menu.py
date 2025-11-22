
"""Enhanced Main Menu for Pride of Code with retro-pixel aesthetic and full feature set.
Implements brass-and-black color scheme with rainbow pride accents, pixel fonts, 
8-bit chime support, and background animations.
"""

import pygame
import math
import random
from typing import List, Optional
from core.state_manager import State
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLUE, COLOR_GOLD, 
                   COLOR_TEXT, COLOR_BG)
from ui.enhanced_retro_button import EnhancedRetroButton, AnimatedPixelButton


class EnhancedMainMenu(State):
    """Enhanced main menu with comprehensive retro-pixel design and animations."""
    
    def __init__(self, manager, game):
        self.manager = manager
        self.game = game
        
        # Color scheme: brass-and-black with rainbow pride accents
        self.colors = {
            'brass': (255, 184, 28),      # Gold/brass
            'black': (20, 20, 30),        # Dark background
            'white': (240, 240, 240),     # Clean text
            'rainbow': [                  # Pride colors
                (228, 3, 3),      # Red
                (255, 140, 0),    # Orange  
                (255, 237, 0),    # Yellow
                (0, 128, 38),     # Green
                (0, 77, 255),     # Blue
                (117, 7, 135),    # Purple
            ],
            'accent': (46, 94, 170),      # Casa Grande blue
            'field_green': (34, 139, 34), # Field green
            'stadium_gray': (80, 80, 90)  # Stadium gray
        }
        
        # Fonts - try to use pixel fonts for retro aesthetic
        try:
            self.font_title = pygame.font.Font(None, 64)  # Large pixel font
            self.font_large = pygame.font.Font(None, 32)  
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
        except:
            # Fallback to system fonts
            self.font_title = pygame.font.SysFont('courier', 64, bold=True)
            self.font_large = pygame.font.SysFont('courier', 32, bold=True)
            self.font_medium = pygame.font.SysFont('courier', 24)
            self.font_small = pygame.font.SysFont('courier', 18)
        
        # Initialize UI elements
        self._create_buttons()
        
        # Animation states
        self.title_animation = 0.0
        self.background_animation = 0.0
        self.pixel_marchers = []
        self._create_marchers()
        
        # Sound system (8-bit chimes)
        self.sound_enabled = True
        self.last_sound_time = 0
        
        # Particle effects for celebration
        self.particles = []
        
        # Menu state
        self.current_selection = 0
        self.animation_intensity = 0
        
        # Retro bowl elements
        self._create_stadium_elements()
        
    def _create_buttons(self):
        """Create main menu buttons with retro styling."""
        button_width = 320
        button_height = 64
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        start_y = 300
        spacing = 80
        
        # Main menu buttons
        self.buttons = [
            AnimatedPixelButton(
                button_x, start_y, button_width, button_height,
                "START SEASON", 
                color=self.colors['brass'],
                animation_type="pulse",
                on_click=lambda: self._navigate_to_level_select()
            ),
            AnimatedPixelButton(
                button_x, start_y + spacing, button_width, button_height,
                "CONTINUE",
                color=self.colors['accent'],
                animation_type="march",
                on_click=lambda: self._navigate_to_continue()
            ),
            AnimatedPixelButton(
                button_x, start_y + spacing * 2, button_width, button_height,
                "SETTINGS",
                color=(100, 100, 100),
                animation_type="sparkle",
                on_click=lambda: self._navigate_to_settings()
            ),
            AnimatedPixelButton(
                button_x, start_y + spacing * 3, button_width, button_height,
                "ABOUT",
                color=(60, 60, 60),
                animation_type="pulse",
                on_click=lambda: self._navigate_to_about()
            ),
            AnimatedPixelButton(
                button_x, start_y + spacing * 4, button_width, button_height,
                "QUIT",
                color=(120, 40, 40),
                animation_type="sparkle",
                on_click=lambda: self._quit_game()
            )
        ]
        
        # Set up keyboard navigation
        self.current_selection = 0
        if self.buttons:
            self.buttons[0].set_focused(True)
            
    def _create_marchers(self):
        """Create pixel art marching band members for background animation."""
        for i in range(12):
            marcher = {
                'x': -100 - (i * 60),  # Start off-screen
                'y': 180 + (i % 3) * 25,  # Alternating heights
                'speed': 1.0 + random.random() * 0.5,
                'color': self.colors['rainbow'][i % len(self.colors['rainbow'])],
                'instrument': random.choice(['trumpet', 'drum', 'flute', 'sax', 'flag']),
                'size': 8 + random.randint(0, 4)
            }
            self.pixel_marchers.append(marcher)
            
    def _create_stadium_elements(self):
        """Create stadium background elements for retro bowl theme."""
        self.stadium_elements = []
        
        # Create stadium tiers
        for i in range(5):
            tier = {
                'y': 80 + i * 20,
                'width': 400 - i * 60,
                'color': (60 + i * 5, 60 + i * 5, 70 + i * 5)
            }
            self.stadium_elements.append(tier)
            
        # Create field lines
        self.field_lines = []
        for i in range(0, WINDOW_WIDTH, 40):
            self.field_lines.append(i)
            
    def _play_chime(self, frequency=440):
        """Play 8-bit chime sound (placeholder for actual audio implementation)."""
        # This would integrate with the actual audio system
        # For now, just print to indicate sound would play
        if self.sound_enabled:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_sound_time > 100:  # Prevent sound spam
                print(f"\u266a 8-bit chime at {frequency}Hz")
                self.last_sound_time = current_time
                
    def _navigate_to_level_select(self):
        """Navigate to level select screen."""
        self._play_chime(523)  # C5 note
        self.manager.switch('level_select')
        
    def _navigate_to_continue(self):
        """Navigate to continue screen (load saved game)."""
        self._play_chime(440)  # A4 note
        # Would integrate with save system
        self.manager.switch('level_select')
        
    def _navigate_to_settings(self):
        """Navigate to settings screen."""
        self._play_chime(349)  # F4 note
        self.manager.switch('settings')
        
    def _navigate_to_about(self):
        """Navigate to about screen."""
        self._play_chime(293)  # D4 note
        self.manager.switch('about')
        
    def _quit_game(self):
        """Quit the game."""
        self._play_chime(220)  # A3 note
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
    def enter(self, **params):
        """Called when entering this state."""
        self.animation_intensity = 0
        self.particles.clear()
        
    def handle_event(self, ev):
        """Handle input events with full keyboard support."""
        # Handle button events
        for button in self.buttons:
            if button.handle_event(ev):
                return
                
        # Keyboard navigation
        if ev.type == pygame.KEYDOWN:
            old_selection = self.current_selection
            
            if ev.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.buttons)
                self._update_selection()
                self._play_chime(440)
                
            elif ev.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.buttons)
                self._update_selection()
                self._play_chime(440)
                
            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_SPACE:
                if self.buttons[self.current_selection].on_click:
                    self.buttons[self.current_selection].on_click()
                    
            elif ev.key == pygame.K_ESCAPE:
                self._quit_game()
                
            # Accessibility shortcuts
            elif ev.key == pygame.K_1:
                self.current_selection = 0
                self._update_selection()
                self.buttons[0].on_click()
            elif ev.key == pygame.K_2:
                self.current_selection = 1
                self._update_selection()
                self.buttons[1].on_click()
            elif ev.key == pygame.K_3:
                self.current_selection = 2
                self._update_selection()
                self.buttons[2].on_click()
            elif ev.key == pygame.K_4:
                self.current_selection = 3
                self._update_selection()
                self.buttons[3].on_click()
            elif ev.key == pygame.K_5:
                self.current_selection = 4
                self._update_selection()
                self.buttons[4].on_click()
                
    def _update_selection(self):
        """Update keyboard focus selection."""
        for i, button in enumerate(self.buttons):
            button.set_focused(i == self.current_selection)
            
    def update(self, dt):
        """Update animations and effects."""
        # Update title animation
        self.title_animation += dt * 2
        
        # Update background animations
        self.background_animation += dt
        
        # Update pixel marchers
        for marcher in self.pixel_marchers:
            marcher['x'] += marcher['speed']
            if marcher['x'] > WINDOW_WIDTH + 100:
                marcher['x'] = -100 - random.randint(0, 200)
                marcher['y'] = 180 + random.randint(-20, 40)
                marcher['color'] = random.choice(self.colors['rainbow'])
                marcher['instrument'] = random.choice(['trumpet', 'drum', 'flute', 'sax', 'flag'])
                
        # Update buttons
        for button in self.buttons:
            button.update(dt)
            
        # Update particles
        self._update_particles(dt)
        
        # Update animation intensity for visual effects
        self.animation_intensity = min(1.0, self.animation_intensity + dt * 2)
        
        # Update stadium elements
        self._update_stadium_elements(dt)
        
    def _update_particles(self, dt):
        """Update particle effects."""
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        # Update existing particles
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 200 * dt  # Gravity
            particle['life'] -= dt
            particle['rotation'] += particle['rotation_speed'] * dt
            
        # Occasionally create new particles for ambient effect
        if random.random() < 0.03:
            self._create_particle(WINDOW_WIDTH // 2, 100)
            
    def _update_stadium_elements(self, dt):
        """Update stadium background elements."""
        # Animate stadium tiers
        for tier in self.stadium_elements:
            tier['width'] += math.sin(self.background_animation * 2 + tier['y'] * 0.01) * 0.5
            
    def _create_particle(self, x, y, color=None):
        """Create a new particle."""
        if color is None:
            color = random.choice(self.colors['rainbow'])
            
        particle = {
            'x': x + random.randint(-20, 20),
            'y': y + random.randint(-20, 20),
            'vx': random.uniform(-50, 50),
            'vy': random.uniform(-100, -50),
            'color': color,
            'life': random.uniform(1.0, 3.0),
            'size': random.randint(2, 6),
            'rotation': 0,
            'rotation_speed': random.uniform(-180, 180)
        }
        self.particles.append(particle)
        
    def draw(self, surface):
        """Render the enhanced main menu."""
        # Draw background
        self._draw_background(surface)
        
        # Draw animated elements
        self._draw_stadium_background(surface)
        self._draw_field(surface)
        self._draw_marchers(surface)
        self._draw_particles(surface)
        
        # Draw UI elements
        self._draw_title(surface)
        self._draw_rainbow_banner(surface)
        self._draw_buttons(surface)
        self._draw_footer(surface)
        
        # Draw pride elements
        self._draw_pride_flags(surface)
        
    def _draw_background(self, surface):
        """Draw animated background."""
        # Base background
        surface.fill(self.colors['black'])
        
        # Animated pixel grid
        grid_offset = int(self.background_animation * 20) % 40
        for x in range(-40, WINDOW_WIDTH + 40, 40):
            for y in range(-40, WINDOW_HEIGHT + 40, 40):
                if (x + y + grid_offset) % 80 == 0:
                    pygame.draw.rect(surface, (30, 30, 40), (x, y, 2, 2))
                    
    def _draw_stadium_background(self, surface):
        """Draw stadium background with tiers."""
        # Draw stadium tiers
        for tier in self.stadium_elements:
            tier_rect = pygame.Rect(
                WINDOW_WIDTH // 2 - tier['width'] // 2,
                tier['y'],
                tier['width'],
                15
            )
            pygame.draw.rect(surface, tier['color'], tier_rect)
            
        # Draw stadium details
        self._draw_stadium_silhouette(surface)
        
    def _draw_stadium_silhouette(self, surface):
        """Draw stadium silhouette in background."""
        # Simple stadium shape
        stadium_color = self.colors['stadium_gray']
        
        # Stadium outline
        points = [
            (100, WINDOW_HEIGHT - 80),
            (100, WINDOW_HEIGHT - 200),
            (200, WINDOW_HEIGHT - 250),
            (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 250),
            (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 200),
            (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 80)
        ]
        pygame.draw.polygon(surface, stadium_color, points)
        
        # Add stadium details
        for i in range(5):
            y = WINDOW_HEIGHT - 180 + i * 20
            pygame.draw.line(surface, (100, 100, 110), (120, y), (WINDOW_WIDTH - 120, y), 1)
            
    def _draw_field(self, surface):
        """Draw football field in background."""
        # Field
        field_rect = pygame.Rect(150, WINDOW_HEIGHT - 160, WINDOW_WIDTH - 300, 50)
        pygame.draw.rect(surface, self.colors['field_green'], field_rect)
        
        # Field lines
        for x in self.field_lines:
            if 150 <= x <= WINDOW_WIDTH - 150:
                pygame.draw.line(surface, (255, 255, 255), (x, WINDOW_HEIGHT - 160), (x, WINDOW_HEIGHT - 110), 1)
                
        # Yard markers
        for i in range(0, WINDOW_WIDTH, 100):
            if 150 <= i <= WINDOW_WIDTH - 150:
                pygame.draw.line(surface, (255, 255, 255), (i, WINDOW_HEIGHT - 160), (i, WINDOW_HEIGHT - 155), 2)
                pygame.draw.line(surface, (255, 255, 255), (i, WINDOW_HEIGHT - 115), (i, WINDOW_HEIGHT - 110), 2)
                
    def _draw_marchers(self, surface):
        """Draw animated pixel art marching band."""
        for marcher in self.pixel_marchers:
            self._draw_pixel_marcher(surface, marcher['x'], marcher['y'], 
                                   marcher['color'], marcher['instrument'], marcher['size'])
                                   
    def _draw_pixel_marcher(self, surface, x, y, color, instrument, size):
        """Draw a single pixel art marcher."""
        if x < -50 or x > WINDOW_WIDTH + 50:
            return
            
        # Head
        pygame.draw.rect(surface, (220, 200, 180), (x - size//2, y - size, size, size//2))
        
        # Body
        pygame.draw.rect(surface, color, (x - size//2, y - size//2, size, size))
        
        # Legs (animated)
        leg_offset = int(math.sin(self.background_animation * 5 + x * 0.1) * size//4)
        pygame.draw.rect(surface, (60, 60, 80), (x - size//3, y + size//2, size//3, size//2 + leg_offset))
        pygame.draw.rect(surface, (60, 60, 80), (x, y + size//2, size//3, size//2 - leg_offset))
        
        # Instrument
        if instrument == 'trumpet':
            pygame.draw.rect(surface, self.colors['brass'], (x + size, y - size//4, size, size//4))
            pygame.draw.circle(surface, self.colors['brass'], (x + size*2, y - size//8), size//3)
        elif instrument == 'drum':
            pygame.draw.rect(surface, (139, 69, 19), (x - size, y - size//4, size//2, size//2))
            pygame.draw.rect(surface, (255, 255, 255), (x - size, y - size//4, size//2, size//8))
        elif instrument == 'flag':
            pygame.draw.rect(surface, (100, 100, 100), (x + size, y - size, size//4, size))
            pygame.draw.polygon(surface, color, [
                (x + size + size//4, y - size),
                (x + size + size//4 + size//2, y - size + size//4),
                (x + size + size//4, y - size + size//2)
            ])
            
    def _draw_particles(self, surface):
        """Draw particle effects."""
        for particle in self.particles:
            alpha = particle['life'] / 3.0  # Fade out
            size = int(particle['size'] * alpha)
            if size > 0:
                # Create a surface for the particle with alpha
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*particle['color'], int(255 * alpha))
                pygame.draw.rect(particle_surf, color, (0, 0, size * 2, size * 2))
                surface.blit(particle_surf, (particle['x'] - size, particle['y'] - size))
                
    def _draw_title(self, surface):
        """Draw animated title with retro styling."""
        # Calculate title animation
        pulse = int(abs(math.sin(self.title_animation)) * 5 * self.animation_intensity)
        
        # Title shadow
        shadow_offset = 4
        title_shadow = self.font_title.render('PRIDE OF CODE', True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + shadow_offset, 80 + shadow_offset))
        surface.blit(title_shadow, shadow_rect)
        
        # Main title with rainbow effect
        title_text = 'PRIDE OF CODE'
        total_width = 0
        char_surfaces = []
        
        # Create rainbow text
        for i, char in enumerate(title_text):
            color = self.colors['rainbow'][i % len(self.colors['rainbow'])]
            char_surf = self.font_title.render(char, True, color)
            char_surfaces.append(char_surf)
            total_width += char_surf.get_width()
            
        # Center and draw rainbow text
        start_x = WINDOW_WIDTH // 2 - total_width // 2
        current_x = start_x
        
        for i, (char_surf, char) in enumerate(zip(char_surfaces, title_text)):
            char_y = 80 + int(math.sin(self.title_animation * 2 + i * 0.5) * pulse)
            surface.blit(char_surf, (current_x, char_y))
            current_x += char_surf.get_width()
            
        # Subtitle
        subtitle = self.font_medium.render('Marching Band Programming Adventure', True, self.colors['white'])
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 140))
        surface.blit(subtitle, subtitle_rect)
        
        # Retro bowl subtitle
        bowl_subtitle = self.font_small.render('Retro Bowl Edition', True, self.colors['brass'])
        bowl_subtitle_rect = bowl_subtitle.get_rect(center=(WINDOW_WIDTH // 2, 170))
        surface.blit(bowl_subtitle, bowl_subtitle_rect)
        
    def _draw_rainbow_banner(self, surface):
        """Draw rainbow pride banner below title."""
        banner_y = 200
        banner_height = 8
        
        for i, color in enumerate(self.colors['rainbow']):
            x = WINDOW_WIDTH // 2 - 200 + i * (400 // len(self.colors['rainbow']))
            width = 400 // len(self.colors['rainbow']) + 1
            pygame.draw.rect(surface, color, (x, banner_y, width, banner_height))
            
        # Banner border
        pygame.draw.rect(surface, self.colors['brass'], 
                        (WINDOW_WIDTH // 2 - 202, banner_y - 2, 404, banner_height + 4), 2)
                        
    def _draw_buttons(self, surface):
        """Draw all menu buttons."""
        for button in self.buttons:
            button.draw(surface)
            
    def _draw_footer(self, surface):
        """Draw footer information."""
        # Version info
        version_text = "v1.0 | Learn Python Through Marching Band"
        version_surf = self.font_small.render(version_text, True, (100, 100, 100))
        version_rect = version_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        surface.blit(version_surf, version_rect)
        
        # Controls hint
        controls_text = "Use \u2191\u2193 or ENTER to navigate | ESC to quit"
        controls_surf = self.font_small.render(controls_text, True, (80, 80, 80))
        controls_rect = controls_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 10))
        surface.blit(controls_surf, controls_rect)
        
    def _draw_pride_flags(self, surface):
        """Draw small pride flag decorations."""
        flag_positions = [
            (100, 250), (WINDOW_WIDTH - 100, 250),
            (100, WINDOW_HEIGHT - 150), (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 150)
        ]
        
        for x, y in flag_positions:
            # Draw small pride flag
            for i, color in enumerate(self.colors['rainbow']):
                flag_y = y + i * 4
                pygame.draw.rect(surface, color, (x, flag_y, 20, 4))
            # Flag pole
            pygame.draw.rect(surface, (100, 100, 100), (x - 2, y - 10, 2, 40))
